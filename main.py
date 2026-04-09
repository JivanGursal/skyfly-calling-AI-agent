from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from database import init_db, Lead, get_db
from pydantic import BaseModel

app = FastAPI(title="Skyfly AI Backend")

# DB Initialize karein
init_db()

# Pydantic Model for Vapi Tool
class LeadRequest(BaseModel):
    name: str
    service: str
    contact: str
    budget: str = "Not Specified"

@app.get("/")
def home():
    return {"status": "Skyfly API is Live"}

# Vapi calls this endpoint
@app.post("/collect-lead")
async def collect_lead(request: LeadRequest, db: Session = Depends(get_db)):
    new_lead = Lead(
        customer_name=request.name,
        service_interested=request.service,
        contact_info=request.contact,
        budget=request.budget
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return {"message": "Lead saved successfully", "lead_id": new_lead.id}

# Dashboard calls this endpoint
@app.get("/view-leads")
def view_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return leads
