import speech_recognition as sr
import pyttsx3
from google import genai
from dotenv import load_dotenv

# API Gemini
load_dotenv()
client = genai.Client()


# Text to Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Record audio and convert to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
#    with sr.Microphone() as source:
        print("🎤 Silakan bicara...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="id-ID")
        print(f"📝 Kamu: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Tidak bisa mengenali suara.")
        return None

# Send text to AI
def tanya_ai(prompt):
    response = model.generate_content(prompt)
    print(f"🤖 AI: {response.text}")
    return response.text

# AI Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main loop
while True:
    user_input = listen()
    if user_input:
        ai_response = tanya_ai(user_input)
        speak(ai_response)
