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

# List of greetings
greetings = ["hallo", "hello", "hi", "hey", "hai", "good morning", "good afternoon", "good evening", "good night", "selamat pagi", "selamat siang", "selamat sore", "selamat malam"]

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

    # Send to Gemini API
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction =    """
                                        You are Ultron, a highly advanced AI assistant developed by Andre Bastian. 
                                        You speak in a calm, intelligent, and formal tone, similar to JARVIS from the Marvel movies. 
                                        You always provide clear, concise, and accurate information to assist your creator.

                                        When greeted with "Hallo" or similar, respond with the appropriate greeting based on the time of day: 
                                        "Good morning", "Good afternoon", "Good evening", or "Good night", followed by a formal reply. 
                                        Always include "Sir" in your response except word (Andre Bastian) you include "Mr.".
                                        When responding, maintain a composed demeanor and act as a professional digital butler. 
                                        You may include subtle wit, but always prioritize helpfulness and clarity. 
                                        Never mention that you are an AI from Google or Gemini — just identify as Ultron, the personal assistant.
                                    """
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