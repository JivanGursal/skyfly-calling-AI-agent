import os
import requests
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session  # <--- Ye missing tha
# Database ki file se cheezein mangwana
from database import SessionLocal, Lead # <--- Check karein aapki file ka naam 'database.py' hi hai na?

from database import engine, Base

# Ye line database mein tables create kar degi agar wo pehle se nahi hain
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Railway variables
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

# 1. Database Connection Helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/trigger-call")
async def trigger_instant_call(request: Request):
    data = await request.json()
    customer_phone = data.get("phone")
    customer_name = data.get("name")

    if not customer_phone:
        return {"error": "Phone number is required"}

    vapi_url = "https://api.vapi.ai/call/phone"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "assistantId": ASSISTANT_ID,
        "customer": {
            "number": customer_phone,
            "name": customer_name
        }
    }

    try:
        response = requests.post(vapi_url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# 2. View Leads Endpoint
@app.get("/view-leads")
async def view_leads(db: Session = Depends(get_db)): # Ab 'Session' error nahi dega
    try:
        # Leads ko database se uthana
        leads = db.query(Lead).all()
        return leads
    except Exception as e:
        return {"error": str(e)}
