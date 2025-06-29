# gemini_utils.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env에서 GEMINI_API_KEY 불러오기
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro-latest")

def generate_mood(feeling, city):
    prompt = (
        f"Given the user's current feeling '{feeling}' and the city '{city}', "
        "generate a concise 3-5 word English mood phrase that captures the combined vibe, "
        "suitable for music playlist recommendations."
    )
    try:
        response = model.generate_content(prompt)
        mood = response.text.strip()
        print(f"✅ Gemini returned mood: {mood}")
        return mood
    except Exception as e:
        print(f"❌ Error generating mood: {e}")
        return "Calm reflective mood"
