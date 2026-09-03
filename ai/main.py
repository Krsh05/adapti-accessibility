from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from intent import detect_intent
from adaptation_ai import determine_adaptation


app = FastAPI(
    title="ADAPTI AI",
    description="AI engine for adaptive accessibility",
    version="1.0.0"
)


# Enable CORS so the frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "ADAPTI AI is running",
        "status": "ok"
    }


@app.post("/intent")
def get_intent(data: UserInput):
    return detect_intent(data.text)


@app.post("/adapt")
def get_adaptation(data: UserInput):
    return determine_adaptation(data.text)


@app.post("/analyze")
def analyze_user(data: UserInput):
    intent = detect_intent(data.text)
    adaptation = determine_adaptation(data.text)

    return {
        "input": data.text,
        "intent": intent,
        "adaptation": adaptation
    }