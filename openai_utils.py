from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mood(feeling, city):
    prompt = (
        f"Given the user's current feeling '{feeling}' and the city '{city}', "
        "generate a concise 3-5 word English mood phrase that captures the combined vibe, "
        "suitable for music playlist recommendations."
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
        print(f"✅ OpenAI returned mood: {mood}")
        return mood
    except Exception as e:
        print(f"❌ Error generating mood: {e}")
        return "Calm reflective mood"
```
