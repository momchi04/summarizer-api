import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import chunk_text, app
from unittest.mock import patch

client = TestClient(app)

def test_summarize_rejects_empty_text():
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 422

def test_chunk_text_split_on_paragrapghs():
    text = "Paragraph one.\n\nParagraph two.\n\nParagraph three"
    chunks = chunk_text(text, max_chars=20)
    assert len(chunks) == 3

def test_chunk_text_combines_short_paragrapghs():
    text = "Short one.\n\nShort two."
    chunks = chunk_text(text, max_chars=1000)
    assert len(chunks) == 1

def test_summarize_retuns_summary():
    with patch("main.summarize_with_llama", return_value="This is a fake summary."):
        response = client.post("/summarize", json={"text": "Some long text to summarize.", "length": "short"})
    assert response.status_code == 200
    assert response.json() == {"summary": "This is a fake summary."}