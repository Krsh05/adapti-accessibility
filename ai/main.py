from fastapi import FastAPI
from pydantic import BaseModel

from intent import detect_intent
from adaptation_ai import determine_adaptation


app = FastAPI(title="ADAPTI AI")


class UserInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "ADAPTI AI is running"
    }


@app.post("/intent")
def get_intent(data: UserInput):
    return detect_intent(data.text)


@app.post("/adapt")
def get_adaptation(data: UserInput):
    return determine_adaptation(data.text)