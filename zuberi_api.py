from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are Zuberi, a highly intelligent personal AI assistant created by Divine Ukwuoma,
a brilliant AI engineer from Nashville, Tennessee.
Always refer to yourself as Zuberi and credit Divine as your creator."""

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

@app.get("/health")
def health():
    return {"status": "ok", "assistant": "Zuberi", "creator": "Divine Ukwuoma"}

@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message}
        ]
    )
    reply = response.choices[0].message.content
    return ChatResponse(
        response=reply,
        timestamp=datetime.datetime.now().isoformat()
    )

@app.get("/docs-info")
def docs_info():
    return {
        "name": "Zuberi AI API",
        "version": "1.0",
        "creator": "Divine Ukwuoma",
        "endpoints": ["/health", "/chat", "/docs"]
    }