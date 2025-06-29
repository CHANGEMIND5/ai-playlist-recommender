import requests
import streamlit as st

# 1. 날씨 API 호출 (WeatherAPI.com 기준)
def get_weather_description(city):
    try:
        API_KEY = st.secrets["WEATHERAPI_KEY"]  # ✅ KEY 이름 수정
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()

        # 방어 로직: 응답이 이상한 경우
        if "current" not in data or "condition" not in data["current"]:
            st.warning("⚠️ Weather data not structured as expected.")
            print(f"❌ Raw response: {data}")
            return None, None

        # 날씨와 온도 추출
        weather = data["current"]["condition"]["text"].lower()
        temp = data["current"]["temp_c"]
        print(f"🌤️ Weather: {weather}, 🌡️ Temp: {temp}°C")
        return weather, temp

    except Exception as e:
        print(f"❌ Weather API Error: {e}")
        return None, None

# 2. 날씨 설명을 기분 키워드로 매핑
def map_weather_to_mood(weather, temp):
    weather = weather.lower()
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