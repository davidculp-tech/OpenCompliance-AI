OpenCompliance AI 🛡️
NIST 800-53 Rev. 5 Assessment Engine
OpenCompliance AI is a lightweight, local-first GRC tool designed to track security control maturity against the NIST 800-53 framework.

## 📦 Requirements
- **Python 3.10+** https://www.python.org/downloads/
- **FastAPI**: `pip install fastapi`
- **Uvicorn**: `pip install uvicorn`
- **SQLModel**: `pip install sqlmodel`
- **Ollama**: https://ollama.com/download for AI analysis features
- **NIST_SP-800-53_rev5_catalog_load.csv**: https://csrc.nist.gov/Projects/risk-management/sp800-53-controls/downloads

### ✨ AI Audit Assistant
The dashboard includes an optional AI-driven expert review feature:
- **Expert Feedback**: Uses `mistral-nemo` via Ollama to analyze implementation statements.
- **Auditor Simulation**: The AI evaluates your statement against the specific NIST Control ID to provide a 2-sentence sufficiency opinion.
- **Local & Private**: All analysis happens on your local machine; no data is sent to external clouds.

## 📊 Maturity Model Definition
The assessment uses a 5-tier maturity scale to quantify risk:

| Score | Status | Definition |
|-------|--------|------------|
| 1 | **FAIL** | **Initial**: Processes are ad-hoc, disorganized, or undocumented. |
| 2 | **FAIL** | **Managed**: Processes are documented but performed inconsistently. |
| 3 | **PARTIAL** | **Defined**: Processes are standardized and integrated into the org. |
| 4 | **PASS** | **Measured**: Processes are monitored with specific performance metrics. |
| 5 | **PASS** | **Optimized**: Continuous improvement is automated and integrated. |

## ⚠️ Maintenance & Troubleshooting
- **Database Reset**: If the NIST CSV or database schema changes, delete `backend/data/compliance.db` and restart Uvicorn to force a re-seed.
- **Port Conflict**: If port `8000` is in use, start Uvicorn with `--port 8001` and update the `fetch` URLs in `index.html`.

🚀 Quick Start
Prepare Data: Ensure NIST_SP-800-53_rev5_catalog_load.csv is in the backend/ folder. Rename the downloaded file to match NIST_SP-800-53_rev5_catalog_load.csv exactly so the backend can find it.

Launch Backend:

Bash

cd backend
uvicorn main:app --reload
Open Dashboard: Launch index.html in any modern web browser.
FastAPI: http://127.0.0.1:8000/docs#/

🛠️ Key Features
Live NIST Reference: Click any Control ID in your history to pull official NIST requirements, supplemental guidance, and related controls directly from the local database.

Maturity Scoring: Track progress using a 1-5 maturity scale (Initial to Optimized).

Dynamic Status Badges: Automatic "PASS/FAIL/PARTIAL" labeling based on your scores.

Remediation Mapping: Integrated plan tracking for failed or partial controls.

Professional Reporting: Generate an instant PDF Audit Report of your current posture.

📂 Architecture
Frontend: Tailwind CSS & Vanilla JavaScript (No heavy frameworks).

Backend: Python FastAPI with SQLModel (SQLite).

Database: Automatic seeding from NIST CSV files upon first launch.

📖 How to Use
Search: Use the ID input box to search for a control. A scrollable dropdown will appear with matches from the NIST library.

Assess: Enter your Implementation Statement. If the score is below 4, document your path to compliance in the Remediation Plan.

Review: Use the History table to see your progress. Click the IDs to double-check the "Wealth of Info" provided by the NIST modal to ensure your statement matches the requirement.

Export: Click "Export PDF" to provide a hard copy for auditors or management.

💡 Final Maintenance Tips
keep these three points in mind for long-term use:

Ollama Models: If you want to try different "AI personalities," you can change model='mistral-nemo' in main.py to other models you've downloaded (like llama3 or phi3).

Model Availability: If the "Run AI Analysis" button ever fails in the future, the first thing to check is if the Ollama application is running in your system tray.

Refining Prompts: You can tweak the "Auditor" instructions in main.py if you want the AI to be stricter or provide more detailed technical steps for remediation.