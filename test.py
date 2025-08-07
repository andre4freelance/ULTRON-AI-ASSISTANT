from google import genai
from google.genai import types
from datetime import datetime
from dotenv import load_dotenv

# API Gemini
load_dotenv()
client = genai.Client()


# Date
def get_time_based_greeting():
    now = datetime.now().hour
    if 5 <= now < 12:
        return "morning"
    elif 12 <= now < 17:
        return "afternoon"
    elif 17 <= now < 21:
        return "evening"
    else:
        return "night"

# User input
user_prompt = input("Ultron online: ")
 
# Greetings list
greetings = ["hallo", "hello", "hi", "hey", "hai", "selamat pagi", "selamat siang", "selamat sore", "selamat malam"]

# Check greetings
normalized_prompt = user_prompt.lower().strip()
if any(normalized_prompt.startswith(greet) for greet in greetings):
    time_greeting = get_time_based_greeting()
    user_prompt += f" (this greeting was issued in the {time_greeting})"

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction = """
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

# AI Response
for chunk in response:
    print(chunk.text, end="")