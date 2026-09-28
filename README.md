# beam-chatbot
Beam RAG Chatbot — Interactive AI Assistant for Saudi Tenders and Opportunities
# Furas (فُرص) — Automated Data Pipeline & Smart Tender Analytics Platform

An end-to-end automated data engineering pipeline and AI-driven tender analytics platform designed to collect, process, unify, and analyze Saudi government tender opportunities from various sources.

---

## 🔗 Project Links & Demos

* **Live Smart Assistant:** [Furas Smart Assistant Streamlit App](https://furas-smart-assistant.streamlit.app)
* **Architecture Standard:** Medallion Architecture (Bronze → Silver → Gold)

---

## 📌 Executive Summary

**Furas (فُرص)** streamlines the extraction and ingestion of Saudi tender data into a unified, clean, and queryable data lakehouse. Built using Databricks, Delta Lake, Snowflake, and Llama 3.3, Furas provides both analytical reporting and an interactive RAG-based AI Assistant for seamless tender inquiry, classification, and status tracking.

---

## ✨ Key Features & Capabilities

1. **Automated Medallion Pipeline:**
   * **Bronze:** Raw data ingestion from Snowflake.
   * **Silver:** Data cleaning, date parsing, field normalization, missing value handling, and dynamic expiration calculations (`effective_status`).
   * **Gold:** Star-schema dimensional model (`fact_tenders`, `dim_agency`, `dim_status`, `dim_category`, `dim_region`, etc.) optimized for OLAP analytics.

2. **RAG-Powered Smart Assistant:**
   * Powered by **Databricks Vector Search** and **Llama 3.3 70B Instruct**.
   * Real-time multilingual support (Arabic & English).
   * Direct link attribution to official tender details on the Etimad platform.
   * Built-in strict guardrails to eliminate hallucination (`I don't have enough information to answer this question.`).

3. **Analytics & Visualization:**
   * Interactive dashboard tracking tender categories, region distribution, estimated values, and active vs. expired opportunities.

---

## 📁 Repository Structure

```text
02_code/
├── 01_data/                 # Sample tender datasets & reference dictionaries
├── 02_src/                  # Application source code
│   ├── app.py               # Streamlit Chatbot Web Application
│   └── beam_rag_notebook_v3.py # Databricks PySpark ETL & RAG Pipeline
├── 03_assets/               # Screenshots, architecture diagrams, and testing logs
│   ├── chatbot_successful_retrieval_test.png
│   └── chatbot_guardrails_no_hallucination_test.png
├── requirements.txt         # Python dependency manifest
└── README.md                # Project documentation & execution guide
```

---

## 🛠️ Tech Stack

* **Data Storage & Warehouse:** Snowflake, Databricks Delta Lake (Unity Catalog)
* **Data Processing & Orchestration:** PySpark, Delta Change Data Feed (CDF)
* **AI / Vector Search:** Databricks Vector Search Client, `databricks-meta-llama-3-3-70b-instruct`
* **Frontend Application:** Streamlit
* **Languages:** Python, SQL, PySpark

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.9+
* Databricks Workspace (with Unity Catalog & Vector Search enabled)
* Snowflake Account with access to `FURAS_DB.GOLD`

### 2. Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Fajjer/beam-chatbot.git
cd beam-chatbot
pip install -r requirements.txt
```

### 3. Running the Chatbot Application

To launch the Streamlit frontend locally:

```bash
streamlit run 02_src/app.py
```

---

## 🔐 Environment Variables & Secrets Setup

For local execution or Streamlit Cloud deployment, configure the following secrets in `.streamlit/secrets.toml`:

```toml
DATABRICKS_HOST = "https://<your-databricks-workspace-url>"
DATABRICKS_TOKEN = "dapi..."
```

---

## 🧪 Testing & Validation Evidence

| Test Scenario | Verification Objective | Result | Screenshot Reference |
|---|---|---|---|
| Successful Retrieval | Querying technical tenders with direct URL citations | PASSED | `03_assets/chatbot_successful_retrieval_test.png` |
| Guardrails & Hallucination | Querying out-of-scope topics (e.g., Space Exploration) | PASSED | `03_assets/chatbot_guardrails_no_hallucination_test.png` |
