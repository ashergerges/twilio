from fastapi import FastAPI, HTTPException, Form
from twilio.rest import Client
from fastapi.responses import Response
import os

app = FastAPI()

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

@app.post("/start-call")
def start_call(
    from_number: str = Form(...),
    to: str = Form(...)
):
    try:
        call = client.calls.create(
            to=to,
            from_=from_number,
            record=True,
            url="https://twilio-780j.onrender.com/twiml"
        )

        return {
            "callSid": call.sid,
            "from": from_number,
            "to": to
        }

    except Exception as e:
        # 👈 ده هيطلع السبب الحقيقي
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

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
