from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Zuberi's knowledge base - facts about Divine
knowledge_base = [
    "Divine Ukwuoma is an AI engineer from Nashville, Tennessee.",
    "Divine studies Computer Engineering at Middle Tennessee State University (MTSU).",
    "Divine's GPA is 3.1 and he graduates in May 2026.",
    "Divine built Jarvis, a voice-activated AI assistant using Groq and Gemini.",
    "Divine is a member of Alpha Phi Alpha Fraternity.",
    "Divine is a Resident Assistant at MTSU.",
    "Divine knows Python, FastAPI, Docker, Kubernetes, and cloud engineering.",
    "Divine's email is ukdivine6@gmail.com.",
    "Divine built Zuberi, his second AI assistant, as part of an ML engineering project.",
    "Divine has experience with RAG systems, transformers, and distributed computing.",
]

# Build the vector index
print("Building Zuberi's memory...")
embeddings = embedder.encode(knowledge_base)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))
print(f"Memory loaded with {len(knowledge_base)} facts!\n")

SYSTEM_PROMPT = """You are Zuberi, a highly intelligent personal AI assistant created by Divine Ukwuoma,
a brilliant AI engineer from Nashville, Tennessee.
Answer questions using the context provided about Divine.
Always refer to yourself as Zuberi and credit Divine as your creator."""

conversation_history = []

def search_memory(query, top_k=3):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = [knowledge_base[i] for i in indices[0]]
    return "\n".join(results)

def chat(user_message):
    # Search memory for relevant facts
    context = search_memory(user_message)
    
    conversation_history.append({"role": "user", "content": user_message})
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Relevant facts about Divine:\n{context}"},
    ] + conversation_history
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

print("Zuberi with memory is online. Type 'quit' to exit.\n")
print("Zuberi with memory is online.")
print("Commands: 'remember: [fact]' to add memory, 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    elif user_input.lower().startswith("remember:"):
        new_fact = user_input[9:].strip()
        knowledge_base.append(new_fact)
        new_embedding = embedder.encode([new_fact])
        index.add(np.array(new_embedding))
        print(f"\nZuberi: Got it! I'll remember that.\n")
    else:
        response = chat(user_input)
        print(f"\nZuberi: {response}\n")