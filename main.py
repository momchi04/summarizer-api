import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import pypdf
import io
from pydantic import BaseModel, Field
import os
from ollama import Client

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_HOST)

app = FastAPI()

class SummarizerRequest(BaseModel):
    text:str = Field(..., min_length=1)
    length: str = "medium"

def chunk_text(text, max_chars=1000):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chars:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_with_llama(text, instruction):
    try:
        response = client.chat(
            model = "llama3.2:3b",
            messages = [
                {
                    "role": "system",
                    "content": "You are a summarization assistant. Only use information explicitly stated in the text you are given. Do not add outside facts, context, or assumptions that are not present in the text. Respond with only the summary itself — do not include any preamble, introduction, or meta-commentary such as 'Here is a summary'."
                },
                {
                    "role": "user", 
                    "content": f"Summarize this {instruction}:\n\n{text}"
                }
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail="The AI model is unavailable. Make sure Ollama is running.")
    return response["message"]["content"]

def generate_summary(text, length):
    length_intructions = {
        "short": "in one sentence",
        "medium": "in 2-3 sentneces",
        "long": "in a detailed paragraph"
    }
    instruction = length_intructions.get(length, length_intructions["medium"])

    if len(text) <= 1000:
        summary = summarize_with_llama(text, instruction)
    else:
        chunks = chunk_text(text, max_chars=1000)
        print(f"Text too long — split into {len(chunks)} chunks")
        chunk_summaries = [summarize_with_llama(chunk, "with a few sentences") for chunk in chunks]
        combined = "\n\n".join(chunk_summaries)
        summary = summarize_with_llama(combined, instruction)
    return summary

@app.post("/summarize")
def summarize(request: SummarizerRequest):
    summary = generate_summary(request.text, request.length)
    return {"summary": summary}

@app.post("/summarize-file")
async def summarize_file(file: UploadFile = File(...), length: str = Form("medium")):
    filename = file.filename.lower()
    contents = await file.read()

    if filename.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(contents))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
    elif filename.endswith(".txt"):
        text = contents.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type: Please upload a .pdf or .txt file.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the uploaded file.")

    summary = await asyncio.to_thread(generate_summary, text, length)
    return {"summary": summary}