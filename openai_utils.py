from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mood(feeling, weather, temp, time_of_day):
    prompt = (
        f"Generate a concise 3-5 word English mood phrase for a music playlist "
        f"based on the user's feeling '{feeling}', current weather '{weather}', temperature '{temp}°C', and time of day '{time_of_day}'. "
        "Reply with ONLY the phrase without any explanation, punctuation, or hashtags."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        mood = response.choices[0].message.content.strip()
        print(f"✅ Raw OpenAI response: {response}")
        print(f"✅ Extracted mood before fallback: '{mood}'")
        return mood
    except Exception as e:
        print(f"❌ Error generating mood: {e}")
        return "Calm reflective mood"


