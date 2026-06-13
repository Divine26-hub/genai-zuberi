from openai import OpenAI
from dotenv import load_dotenv
import os
import datetime
import math
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define Zuberi's tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate e.g. '2 + 2'"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Save a note to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "The note to save"}
                },
                "required": ["note"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_notes",
            "description": "Get all saved notes",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

# Tool implementations
def get_current_time():
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}"

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"{expression} = {result}"
    except:
        return "I couldn't calculate that expression."

def save_note(note):
    with open("zuberi_notes.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {note}\n")
    return f"Note saved successfully!"

def get_notes():
    if not os.path.exists("zuberi_notes.txt"):
        return "No notes saved yet."
    with open("zuberi_notes.txt", "r") as f:
        return f.read()

def run_tool(tool_name, tool_args):
    if tool_name == "get_current_time":
        return get_current_time()
    elif tool_name == "calculate":
        return calculate(tool_args["expression"])
    elif tool_name == "save_note":
        return save_note(tool_args["note"])
    elif tool_name == "get_notes":
        return get_notes()

SYSTEM_PROMPT = """You are Zuberi, a highly intelligent personal AI assistant created by Divine Ukwuoma,
a brilliant AI engineer from Nashville, Tennessee.
You have access to tools - use them when needed.
Always refer to yourself as Zuberi and credit Divine as your creator."""

conversation_history = []

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        tools=tools
    )
    
    message = response.choices[0].message
    
    # Check if Zuberi wants to use a tool
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print(f"\n[Zuberi is using tool: {tool_name}]")
            tool_result = run_tool(tool_name, tool_args)
            
            conversation_history.append(message)
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        
        # Get final response after tool use
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        )
        reply = final_response.choices[0].message.content
    else:
        reply = message.content
    
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

print("Zuberi Agent is online. Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = chat(user_input)
    print(f"\nZuberi: {response}\n")
    