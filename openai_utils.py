from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mood(feeling, city):
    prompt = (
        f"You are an AI that creates music moods. The user is feeling '{feeling}' in '{city}'. "
        "Respond ONLY with a concise 3-5 word English mood phrase suitable for a music playlist. Do not add any explanation."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        mood = response.choices[0].message.content.strip()
        print(f"✅ Raw OpenAI response object: {response}")
        print(f"✅ Extracted mood before fallback check: '{mood}'")
        return mood
    except Exception as e:
        print(f"❌ Error generating mood: {e}")
        return "Calm reflective mood"
