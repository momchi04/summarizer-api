# Summarizer API

A backend API that takes text and returns an AI-generated summary, built locally with FastAPI and Ollama.

## Why this exists

Companies regularly need to condense large amounts of text into something skimmable — customer support tickets, product reviews, meeting transcripts, long articles. This is a small proof-of-concept backend service that does exactly that: send it text (or a PDF/txt file), get back a summary. Built as a learning project to explore backend API design and running LLMs locally.

## Tech stack

- Python 3.12+
- FastAPI — API framework
- Ollama — runs the LLM locally
- Model: llama3.2:3b (small, runs on a normal laptop, no GPU required)
- Uvicorn — server that runs the app
- Docker — optional containerized setup

## How to run it locally

1. Install [Ollama](https://ollama.com) and pull the model: `ollama pull llama3.2:3b`
2. Clone this repo: `git clone https://github.com/momchi04/summarizer-api.git` then `cd summarizer-api`
3. Create and activate a virtual environment: `python -m venv venv` then `source venv/Scripts/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn main:app --reload`
6. API runs at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`

## Run with Docker (alternative to manual setup)

1. Make sure Ollama is running locally with the model pulled: `ollama pull llama3.2:3b`
2. Build the image: `docker build -t summarizer-api .`
3. Run it: `docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 summarizer-api`
4. API available at `http://127.0.0.1:8000`

## Example usage

Summarize raw text:
```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Ollama lets you run open-source AI models locally on your own computer instead of calling a cloud API.", "length": "medium"}'
```

Response:
```json
{"summary":"Ollama is a platform that enables users to run open-source AI models on their own computers, bypassing cloud-based APIs and allowing for local execution."}
```

Summarize an uploaded file:
```bash
curl -X POST http://127.0.0.1:8000/summarize-file \
  -F "file=@test.txt" \
  -F "length=medium"
```

## Roadmap

- [x] Summary length/style options (short/medium/long)
- [x] Handle long documents via chunking (map-reduce summarization)
- [x] Accept file uploads (PDF, .txt)
- [x] Input validation and graceful error handling
- [x] Dockerize for easy deployment
- [ ] Deploy to a live URL (Render/Fly.io) for a public demo
- [ ] Add basic API-key authentication and rate limiting
- [ ] Add automated tests (pytest)