from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class SummarizerRequest(BaseModel):
    text:str
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
    response = ollama.chat(
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
    return response["message"]["content"]

@app.post("/summarize")
def summarize(request: SummarizerRequest):
    length_intructions = {
        "short": "in one sentence",
        "medium": "in 2-3 sentneces",
        "long": "in a detailed paragraph"
    }
    instruction = length_intructions.get(request.length, length_intructions["medium"])

    if len(request.text) <= 1000:
        summary = summarize_with_llama(request.text, instruction)
    else:
        chunks = chunk_text(request.text, max_chars=1000)
        print(f"Text too long — split into {len(chunks)} chunks")
        chunk_summaries = [summarize_with_llama(chunk, "with a few sentences") for chunk in chunks]
        combined = "\n\n".join(chunk_summaries)
        summary = summarize_with_llama(combined, instruction)

    return {"summary": summary}