@app.post("/trigger-call")
async def trigger_instant_call(request: Request, db: Session = Depends(get_db)): # db add kiya
    data = await request.json()
    customer_phone = data.get("phone")
    customer_name = data.get("name")

    if not customer_phone:
        return {"error": "Phone number is required"}

    # --- YE ADD KAREIN: Database mein lead save karna ---
    new_lead = Lead(
        customer_name=customer_name, 
        contact_info=customer_phone,
        service_interested="AI Voice Agent (Website Form)"
    )
    db.add(new_lead)
    db.commit()
    # ---------------------------------------------------

    vapi_url = "https://api.vapi.ai/call/phone"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "assistantId": ASSISTANT_ID,
        "customer": {"number": customer_phone, "name": customer_name}
    }

    try:
        response = requests.post(vapi_url, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Dashboard ki manual entry ke liye ye naya endpoint add karein
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
