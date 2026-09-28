import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.vector_search.client import VectorSearchClient

ENDPOINT_NAME = "beam-tenders-endpoint"
INDEX_NAME = "tenderdatabricks.default.tenders_index"
LLM_MODEL = "databricks-meta-llama-3-3-70b-instruct"

st.set_page_config(page_title="Furas | Smart Assistant", page_icon="💬", layout="centered")

@st.cache_resource
def get_clients():
    host = st.secrets["DATABRICKS_HOST"]
    token = st.secrets["DATABRICKS_TOKEN"]
    w = WorkspaceClient(host=host, token=token)
    vsc = VectorSearchClient(
        workspace_url=host,
        personal_access_token=token,
        disable_notice=True,
    )
    index = vsc.get_index(endpoint_name=ENDPOINT_NAME, index_name=INDEX_NAME)
    return w.serving_endpoints.get_open_ai_client(), index

try:
    client, index = get_clients()
except Exception as e:
    st.error("Failed to connect to the service. Please check your credentials and configuration.")
    st.stop()

st.title("💬 Furas Smart Assistant")
st.caption("Search and query tenders and investment opportunities easily and quickly")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! How can I assist you with searching tenders and opportunities today?"}
    ]

# Session question limit to manage resource usage (20 questions)
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your question here..."):
    if st.session_state.question_count >= 20:
        st.warning("You have reached the maximum limit of 20 questions for this session. Please refresh the page to start a new session.")
    else:
        st.session_state.question_count += 1
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Searching the database..."):
            try:
                # 1. Retrieval
                results = index.similarity_search(
                    query_text=prompt,
                    columns=["TENDER_KEY", "content"],
                    num_results=8,
                )
                data_array = results.get("result", {}).get("data_array", [])
                context_text = "\n\n".join([row[1] for row in data_array])

                # 2. Generation
                system_prompt = (
                    "You are an AI assistant for the Furas (فُرص) platform. "
                    "Answer the user's question strictly based on the provided tender context. "
                    "Always respond in the same language as the question. "
                    "When referencing tenders, include the Tender Name and Link if available. "
                    "If asked for overall analytics or statistics, politely direct the user to the Furas Dashboard. "
                    "If the answer cannot be determined from the context, state that information is not available."
                )

                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {prompt}"},
                    ],
                    temperature=0.1,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = "Sorry, an error occurred while processing your request. Please try again."

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)