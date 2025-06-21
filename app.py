import streamlit as st
import requests
from weather_utils import map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string

# 페이지 설정
st.set_page_config(
    page_title="Skytonees",
    page_icon="🎧",
    layout="centered"
)

# 타이틀 및 설명
st.title("🎵 Skytonees: AI Music Playlist Recommender")
st.markdown("Let us find the perfect playlist for your current **mood**, based on the weather and time 🎶")

# 사용자 입력
city = st.text_input("🌍 Enter your city:", placeholder="e.g., Seoul")

# 🔧 날씨 정보 가져오기
def get_weather_description(city):
    api_key = st.secrets["WEATHERAPI_KEY"]
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

    try:
        res = requests.get(url)
        data = res.json()

        weather = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        return weather, temp
    except Exception as e:
        print(f"❌ Weather API error: {e}")
        return None, None

# 🌤️ 도시 정보가 입력되었을 때 실행
if city:
    weather, temp = get_weather_description(city)

    if weather is None or temp is None:
        st.error("❌ Failed to retrieve weather data. Please check the city name.")
    else:
        # 🕒 시간 및 무드 분석
        local_time = get_local_time(city)
        current_time_str = get_current_time_string(local_time)
        mood_weather = map_weather_to_mood(weather, temp)
        mood_time = get_time_based_mood(local_time)
        combined_mood = f"{mood_weather}, {mood_time}"

        # 💡 정보 박스 출력
        info_html = f"""
        <div style="background-color:#f0f4f8; padding: 15px 20px; border-radius: 12px; margin-top: 20px; font-size:16px;">
        <b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C <br>
        <b>🕒 Local Time in {city}:</b> {current_time_str} <br>
        <b>🎯 Mood:</b> {mood_weather}, {mood_time}
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

        # 🎧 플레이리스트 추천
        st.subheader("🎵 Recommended Playlists:")
        playlists = search_playlist_by_mood(combined_mood)

        if playlists:
            for name, url in playlists:
                card_html = f"""
                <div style="background-color:#ffffff; padding:15px 20px; margin:10px 0; border-radius:10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); font-size:16px;">
                <a href="{url}" target="_blank" style="text-decoration: none; color: #000000;">🎧 {name}</a>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No playlists found for your mood. Try a different city!")

