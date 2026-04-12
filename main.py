import os
import requests
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Lead, engine, Base, init_db

# App start hote hi table ban jayega
init_db()

app = FastAPI()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. WordPress Se Lead Receive karna aur Call milana
@app.post("/trigger-call")
async def trigger_instant_call(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    customer_phone = data.get("phone")
    customer_name = data.get("name")

    if not customer_phone:
        return {"error": "Phone number is required"}

    # Database mein save karna
    new_lead = Lead(
        customer_name=customer_name, 
        contact_info=customer_phone,
        service_interested="AI Voice Agent (Website Form)"
    )
    db.add(new_lead)
    db.commit()

    # Vapi Call Trigger
    vapi_url = "https://api.vapi.ai/call/phone"
    headers = {"Authorization": f"Bearer {VAPI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "assistantId": ASSISTANT_ID,
        "customer": {"number": customer_phone, "name": customer_name}
    }

    try:
        response = requests.post(vapi_url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 2. Dashboard Par Leads Dikhana
@app.get("/view-leads")
async def view_leads(db: Session = Depends(get_db)):
    try:
        leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
        return leads
    except Exception as e:
        return {"error": str(e)}

# 3. Dashboard Se Manual Lead Save karna
@app.post("/collect-lead")
async def collect_lead(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    new_lead = Lead(
        customer_name=data.get("name"),
        service_interested=data.get("service"),
        contact_info=data.get("contact"),
        budget=data.get("budget")
    )
    db.add(new_lead)
    db.commit()
    return {"status": "success"}
