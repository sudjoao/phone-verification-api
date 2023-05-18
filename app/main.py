from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

key = os.getenv('KEY')
secret = os.getenv('SECRET')
sinchVerificationUrl = "https://verification.api.sinch.com/verification/v1/verifications"

class VerificationBody(BaseModel):
    phone: str

class ConfirmBody(BaseModel):
    phone: str
    code: str

app = FastAPI()

@app.post("/send_verification")
async def send_verification(verification_body: VerificationBody) -> dict:
    payload = {
        "identity": {
            "type": "number",
            "endpoint": verification_body.phone
        },
        "method": "sms"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(sinchVerificationUrl, json=payload, headers=headers, auth=(key, secret))

    data = response.json()
    return data

@app.post("/verify_number")
async def verify_number(verification_body: ConfirmBody) -> dict:
    url = sinchVerificationUrl + f'/number/{verification_body.phone}'
    payload = {
        "method": "sms",
        "sms": {
            "code": verification_body.code
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=payload, headers=headers, auth=(key, secret))
    data = response.json()
    return data