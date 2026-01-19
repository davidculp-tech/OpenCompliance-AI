from typing import Optional
from datetime import datetime, timezone
import csv
import os
import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- Models ---
class ControlReference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str = Field(index=True)
    name: str
    control_text: str
    discussion: Optional[str] = None
    related: Optional[str] = None # Added for more info

class Assessment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    audit_year: int
    framework: str = "NIST"
    ref_id: str
    score: int
    implementation_statement: str
    remediation_plan: Optional[str] = None
    category: str = Field(default="General")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssessmentCreate(SQLModel):
    audit_year: int
    ref_id: str
    score: int
    implementation_statement: str
    remediation_plan: Optional[str] = None
    category: str = "General"

# --- Database Setup ---
sqlite_file_name = "../data/compliance.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def seed_reference_library():
    with Session(engine) as session:
        if session.exec(select(ControlReference)).first() is None:
            csv_path = "NIST_SP-800-53_rev5_catalog_load.csv"
            if os.path.exists(csv_path):
                with open(csv_path, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        session.add(ControlReference(
                            identifier=row['identifier'],
                            name=row['name'],
                            control_text=row['control_text'],
                            discussion=row.get('discussion'),
                            related=row.get('related')
                        ))
                session.commit()
                print("✅ NIST Reference Library Loaded.")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    seed_reference_library()

@app.post("/submit-assessment/")
def create_assessment(data: AssessmentCreate):
    with Session(engine) as session:
        stmt = select(Assessment).where(Assessment.ref_id == data.ref_id, Assessment.audit_year == data.audit_year)
        existing = session.exec(stmt).first()
        if existing:
            existing.score, existing.implementation_statement, existing.remediation_plan = data.score, data.implementation_statement, data.remediation_plan
            existing.last_updated = datetime.now(timezone.utc)
        else:
            session.add(Assessment(**data.dict(), framework="NIST"))
        session.commit()
        return {"status": "success"}

@app.get("/history-all/")
def get_all_history():
    with Session(engine) as session:
        return session.exec(select(Assessment).order_by(Assessment.audit_year.desc())).all()

@app.get("/library/search")
def search_library(q: str):
    with Session(engine) as session:
        # Increased limit to 50 so users can scroll through a full family
        statement = select(ControlReference).where(
            (ControlReference.identifier.ilike(f"%{q}%")) | 
            (ControlReference.name.ilike(f"%{q}%"))
        ).limit(50) 
        return session.exec(statement).all()

# NEW: Exact lookup for the Modal
@app.get("/library/get/{ref_id}")
def get_control(ref_id: str):
    with Session(engine) as session:
        result = session.exec(select(ControlReference).where(ControlReference.identifier == ref_id)).first()
        return result or {"error": "Not found"}
        
@app.get("/analyze-compliance/{ref_id}")
def analyze_compliance(ref_id: str, year: int = 2026):
    with Session(engine) as session:
        # Get your implementation notes for this specific ID and year
        record = session.exec(select(Assessment).where(
            Assessment.ref_id == ref_id, 
            Assessment.audit_year == year
        )).first()
        
        if not record: 
            return {"ai_analysis": "Please save your implementation statement first before asking for AI analysis."}
        
        try:
            prompt = (f"As a NIST auditor, review the following for {record.ref_id}: "
                      f"'{record.implementation_statement}'. "
                      f"Is this sufficient? Give a concise 2-sentence expert opinion.")
            
            # This calls your local Mistral model
            response = ollama.chat(model='mistral-nemo', messages=[{'role': 'user', 'content': prompt}])
            return {"ai_analysis": response['message']['content']}
        except Exception as e:
            return {"ai_analysis": f"AI Engine Error: Ensure Ollama is running. ({str(e)})"}