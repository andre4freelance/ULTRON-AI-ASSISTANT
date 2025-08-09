import sys
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key and initialize client
load_dotenv()
client = genai.Client()

# Function to determine time-based greeting
def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

# Load Greetings
def load_greetings(filepath="greetings.txt"):
    with open(filepath, "r") as f:
        return [line.strip().lower() for line in f.readlines()]
greetings = load_greetings()

# File to store conversation history
history_file = "ultron_conversation_log.json"
conversation_log = []

# Load previous log if exists
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        try:
            conversation_log = json.load(f)
        except json.JSONDecodeError:
            conversation_log = []

# Main loop
print("Ultron online. Tell me what you need, Sir. Type 'exit' to shut me down.\n")

while True:
    user_prompt = input("You: ").strip()
    if user_prompt.lower() in ["exit", "quit", "keluar"]:
        print("Ultron: Shutting down. Goodbye, Sir.")
        break

    # Insert time if greeting detected
    normalized_prompt = user_prompt.lower()
    if any(normalized_prompt.startswith(greet) for greet in greetings):
        time_greeting = get_time_based_greeting()
        user_prompt += f" (this greeting was issued in the {time_greeting})"

    # Read system instruction
    with open("system_instruction.txt", "r") as f:
        instruction = f.read()

    # Send to Gemini API
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction =instruction,
        ),
        contents=user_prompt
    )

    # Get response as stream and display
    ultron_reply = ""
    print("Ultron: ", end="", flush=True)
    for chunk in response:
        if hasattr(chunk, "text"):
            print(chunk.text, end="", flush=True)
            ultron_reply += chunk.text
    print()

    # Save to log
    conversation_log.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_prompt,
        "ultron": ultron_reply.strip()
    })

    # Write to JSON file
    with open(history_file, "w") as f:
        json.dump(conversation_log, f, indent=4)