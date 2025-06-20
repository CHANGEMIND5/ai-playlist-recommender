import requests
import streamlit as st

# 1. 날씨 API 호출
def get_weather_description(city):
    try:
        API_KEY = st.secrets["OPENWEATHER_API_KEY"]  # secrets.toml에서 가져오기
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        # 응답 구조 확인 및 방어 처리
        if "current" not in data or "condition" not in data["current"]:
            print(f"❌ Weather API raw response: {data}")
            return None, None

        # 날씨 설명과 기온 추출
        weather = data["current"]["condition"]["text"].lower()
        temp = data["current"]["temp_c"]

        print(f"🌤️ Weather: {weather}, 🌡️ Temp: {temp}°C")
        return weather, temp

    except Exception as e:
        print(f"❌ Weather API Error: {e}")
        return None, None

# 2. 날씨 설명을 기분 키워드로 매핑
def map_weather_to_mood(weather, temp):
    if "sun" in weather or "clear" in weather:
        return "happy, energetic"
    elif "cloud" in weather:
        return "chill, calm, focus"
    elif "rain" in weather or "drizzle" in weather:
        return "sad, mellow, acoustic"
    elif "snow" in weather:
        return "cozy, soft, instrumental"
    elif "storm" in weather or "thunder" in weather:
        return "powerful, cinematic"
    else:
        return "lofi, ambient"

