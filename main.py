from fastapi import FastAPI, Request
from pydantic import BaseModel
from database import init_db, insert_lead

app = FastAPI()

# Database initialize karein
init_db()

class SkyflyLead(BaseModel):
    name: str
    service: str
    contact: str
    budget: str = "Not Specified"

@app.get("/")
async def root():
    return {"message": "Skyfly Technology AI Voice Backend is Running!"}

@app.post("/collect-lead")
async def collect_lead(request: Request):
    # Vapi sends data in a specific format
    payload = await request.json()
    
    # Extracting data from Vapi's tool call structure
    try:
        # Agar aapne Vapi mein tool parameter 'name', 'service', 'contact' rakhe hain
        args = payload["message"]["toolCalls"][0]["function"]["arguments"]
        
        name = args.get("name")
        service = args.get("service")
        contact = args.get("contact")
        budget = args.get("budget", "Not Specified")

        # Database mein save karein
        insert_lead(name, service, contact, budget)
        
        return {
            "results": f"Thank you {name}. Your inquiry for {service} has been recorded. Our team at Skyfly will contact you soon."
        }
    except Exception as e:
        return {"error": str(e), "message": "Failed to extract lead data"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)