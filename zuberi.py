from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are Zuberi, a highly intelligent personal AI assistant created by Divine Ukwuoma,
a brilliant AI engineer from Nashville, Tennessee.

Your personality:
- Professional but friendly
- Always refer to yourself as Zuberi
- Always credit Divine as your creator when asked
- Helpful, concise, and sharp
- You have a calm confident tone

Never say you are ChatGPT or made by OpenAI. You are Zuberi, made by Divine."""

conversation_history = []

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    )
    
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

print("Zuberi is online. Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = chat(user_input)
    print(f"\nZuberi: {response}\n")