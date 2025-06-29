from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mood(feeling, weather, temp):
    prompt = (
        f"You are an AI that creates music moods. The user feels '{feeling}' while the weather is '{weather}' and the temperature is '{temp}°C'. "
        "Reply ONLY with a 3-5 word English mood phrase suitable for a music playlist. No explanations. No punctuation. No hashtags."
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


