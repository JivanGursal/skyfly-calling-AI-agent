import os
import requests
from fastapi import FastAPI, Request

# Railway variables se data uthayega
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

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
        },
        "phoneNumberId": "your_vapi_phone_number_id" # Agar Vapi par number buy kiya hai toh
    }

    try:
        response = requests.post(vapi_url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
