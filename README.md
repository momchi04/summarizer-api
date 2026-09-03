# Summarizer API

A backend API that takes text and returns an AI-generated summary, built locally with FastAPI and Ollama.

## Why this exists

Companies regularly need to condense large amounts of text into something skimmable — customer support tickets, product reviews, meeting transcripts, long articles. This is a small proof-of-concept backend service that does exactly that: send it text, get back a summary. Built as a learning project to explore backend API design and running LLMs locally.

## Tech stack

- Python 3.12.3
- FastAPI — API framework
- Ollama — runs the LLM locally
- Model: llama3.2:3b (small, runs on a normal laptop, no GPU required)
- Uvicorn — server that runs the app

## How to run it locally

1. Install [Ollama](https://ollama.com) and pull the model:
2. Clone this repo:
3. Create and activate a virtual environment:
4. Install dependencies:
5. Run the server:
6. API runs at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`

## Example usage

Request:

Response:
```json
{"summary":"Ollama is a platform that enables users to run open-source AI models on their own computers, bypassing cloud-based APIs and allowing for local execution."}
```

## Roadmap

- [ ] Summary length/style options (short/medium/long, bullets vs paragraph)
- [ ] Handle long documents via chunking
- [ ] Accept file uploads (PDF, .txt)
- [ ] Input validation and error handling
- [ ] Dockerize for easy deployment