import os
import requests
from fastapi import APIRouter, Request, FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = os.getenv("AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")


@app.get("/login")
def login():
    url = (
        f"{TOKEN_URL}?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=kekaapi offline_access&"
    )
    return RedirectResponse(url)


@app.get("/callback")
def callback(request: Request, code: str):
    token_response = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "scope": "kekaapi offline_access"
        }
    )
    tokens = token_response.json()
    # Here you’d store tokens in a database or session
    return tokens
