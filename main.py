import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
from fastapi.responses import Response

load_dotenv()

app = FastAPI()

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

class CallRequest(BaseModel):
    from_number: str
    to: str

@app.post("/start-call")
def start_call(data: CallRequest):
    if not data.from_number or not data.to:
        raise HTTPException(status_code=400, detail="from and to required")

    call = client.calls.create(
        to=data.to,
        from_=data.from_number,
        record=True,  # 🎙️ تسجيل
        url="https://twilio-780j.onrender.com/twiml"  # ✅ الدومين الحقيقي
    )

    return {
        "callSid": call.sid,
        "from": data.from_number,
        "to": data.to
    }

@app.api_route("/twiml", methods=["GET", "POST"])
def twiml():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-EG">
        مكالمة واردة من التطبيق
    </Say>
</Response>
"""
    return Response(content=xml, media_type="application/xml")
