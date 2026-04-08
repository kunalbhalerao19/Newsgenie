from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- ADD THIS
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Import the updated functions from inference.py
from inference import fetch_news, build_prompt, generate_newsletter
from groq import Groq

app = FastAPI(title="Newsletter API")

# ADD CORS MIDDLEWARE (allows your frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allows all origins (including file:// and http://localhost:5500)
    allow_credentials=True,
    allow_methods=["*"],   # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # Allows all headers
)

class GenerateRequest(BaseModel):
    interests: Optional[List[str]] = ["Artificial Intelligence", "Technology", "Startups", "Programming"]
    max_articles: int = 5

class GenerateResponse(BaseModel):
    newsletter: str
    articles_used: int

@app.get("/")
async def root():
    return {"message": "Newsletter API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
async def generate_newsletter_endpoint(request: GenerateRequest):
    # Override USER_INTERESTS temporarily
    import inference
    original = inference.USER_INTERESTS
    inference.USER_INTERESTS = request.interests
    try:
        articles = fetch_news()
    finally:
        inference.USER_INTERESTS = original

    if not articles:
        raise HTTPException(404, "No articles found")

    articles = articles[:request.max_articles]
    prompt = build_prompt(articles)

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise HTTPException(500, "GROQ_API_KEY not set")

    client = Groq(api_key=groq_key)
    newsletter = generate_newsletter(client, prompt)

    if not newsletter:
        raise HTTPException(500, "Newsletter generation failed")

    return GenerateResponse(newsletter=newsletter, articles_used=len(articles))