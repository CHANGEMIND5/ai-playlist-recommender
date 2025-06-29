# gemini_utils.py

from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드 (로컬 개발 시)
load_dotenv()

# OpenAI 클라이언트 생성 (Gemini Key는 OPENAI_API_KEY 로 설정해야 인식됨)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_mood(feeling, city):
    """
    사용자의 기분(feeling)과 도시(city)를 입력받아
    Gemini(OpenAI) 모델을 통해 무드 텍스트를 생성해 반환합니다.
    """
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
        print(f"✅ Gemini returned mood: {mood}")
        return mood

    except Exception as e:
        print(f"❌ Error generating mood: {e}")
        return "Calm reflective mood"  # 에러 시 기본 무드 반환