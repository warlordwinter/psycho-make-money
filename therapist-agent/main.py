from fastapi import FastAPI
from pydantic import BaseModel
from run_pipeline import run_full_therapist_pipeline

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    license: str = "Psychologist"

@app.post("/analyze")
async def analyze_conversation(data: TranscriptRequest):
    result = run_full_therapist_pipeline(data.transcript, data.license)
    return result