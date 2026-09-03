from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class SummarizerRequest(BaseModel):
    text:str

@app.post("/summarize")
def summarize(request: SummarizerRequest):
    response = ollama.chat(
        model = "llama3.2:3b",
        messages = [
            {"role": "user", "content": f"Summarize this in one sentence: {request.text}" }
        ]
    )
    return {"summary": response["message"]["content"]}