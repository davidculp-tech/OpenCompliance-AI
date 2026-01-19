# **OpenCompliance AI 🛡️**

### **NIST 800-53 Rev. 5 Assessment Engine**

OpenCompliance AI is a lightweight, local-first GRC tool designed to track security control maturity against the NIST 800-53 framework.

## **📦 Requirements**

* **Python 3.10+**: [Official Downloads](https://www.python.org/downloads/)  
* **FastAPI**: pip install fastapi  
* **Uvicorn**: pip install uvicorn  
* **SQLModel**: pip install sqlmodel  
* **Ollama**: [Download for AI Features](https://ollama.com/download)  
* **NIST Control Catalog**: [Download CSV](https://csrc.nist.gov/Projects/risk-management/sp800-53-controls/downloads)

## **🚀 Quick Start**

1. **Prepare Data**: Ensure the NIST CSV file is in the backend/ folder.**Note**: Rename your downloaded file to match NIST\_SP-800-53\_rev5\_catalog\_load.csv exactly so the backend can find it.  
2. **Launch Backend**:  
   cd backend  
   uvicorn main:app \--reload

3. **Open Dashboard**: Open index.html in any modern web browser.  
   * **Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## **✨ AI Audit Assistant**

The dashboard includes an optional AI-driven expert review feature:

* **Expert Feedback**: Uses mistral-nemo via Ollama to analyze implementation statements.  
* **Auditor Simulation**: The AI evaluates your statement against the specific NIST Control ID to provide a 2-sentence sufficiency opinion.  
* **Local & Private**: All analysis happens on your local machine; no data is sent to external clouds.

## **📊 Maturity Model Definition**

The assessment uses a 5-tier maturity scale to quantify risk:

| Score | Status | Definition |
| :---- | :---- | :---- |
| 1 | **FAIL** | **Initial**: Processes are ad-hoc, disorganized, or undocumented. |
| 2 | **FAIL** | **Managed**: Processes are documented but performed inconsistently. |
| 3 | **PARTIAL** | **Defined**: Processes are standardized and integrated into the org. |
| 4 | **PASS** | **Measured**: Processes are monitored with specific performance metrics. |
| 5 | **PASS** | **Optimized**: Continuous improvement is automated and integrated. |

## **🛠️ Key Features**

* **Live NIST Reference**: Click any Control ID in your history to pull official requirements, supplemental guidance, and related controls directly from the local database.  
* **Maturity Scoring**: Track progress using a 1-5 maturity scale.  
* **Dynamic Status Badges**: Automatic "PASS/FAIL/PARTIAL" labeling based on your scores.  
* **Remediation Mapping**: Integrated plan tracking for failed or partial controls.  
* **Professional Reporting**: Generate an instant PDF Audit Report of your current posture.

## **📂 Architecture**

* **Frontend**: Tailwind CSS & Vanilla JavaScript (No heavy frameworks).  
* **Backend**: Python FastAPI with SQLModel (SQLite).  
* **Database**: Automatic seeding from NIST CSV files upon first launch.

## **📖 How to Use**

1. **Search**: Use the ID input box to search for a control. A scrollable dropdown will appear with matches from the NIST library.  
2. **Assess**: Enter your Implementation Statement. If the score is below 4, document your path to compliance in the **Remediation Plan**.  
3. **Review**: Use the History table to see your progress. Click IDs to double-check requirements in the modal.  
4. **Export**: Click "Export PDF" to provide a hard copy for auditors or management.

## **⚠️ Maintenance & Troubleshooting**

* **Database Reset**: If the NIST CSV or database schema changes, delete backend/data/compliance.db and restart Uvicorn to force a re-seed.  
* **Port Conflict**: If port 8000 is in use, start Uvicorn with uvicorn main:app \--reload \--port 8001 and update the fetch URLs in index.html.  
* **Ollama Models**: You can change model='mistral-nemo' in main.py to other models like llama3 or phi3.  
* **Model Availability**: Ensure the Ollama application is running in your system tray before clicking "Run AI Analysis."