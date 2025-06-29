# gemini_utils.py

from openai import OpenAI
import os

# Gemini 클라이언트 생성
client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"))

def generate_mood(feeling, city):
    """
    사용자의 기분(feeling)과 도시(city)를 입력받아
    Gemini를 통해 무드 텍스트를 생성해 반환합니다.
    """
    prompt = (
        f"Given the user's current feeling '{feeling}' and the city '{city}', "
        "generate a concise 3-5 word English mood phrase that captures the combined vibe, "
        "suitable for music playlist recommendations."
    )

    try:
        response = client.chat.completions.create(
            model="gemini-1.5-pro-latest",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        mood = response.choices[0].message.content.strip()
        return mood

    except Exception as e:
        print(f"Error generating mood: {e}")
        return "Error generating mood"