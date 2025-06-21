import streamlit as st
from weather_utils import get_weather_description, map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string

# 페이지 설정
st.set_page_config(
    page_title="Skytonees",
    page_icon="🎧",
    layout="centered"
)

# 헤더
st.title("🎵 Skytonees: AI Music Playlist Recommender")
st.markdown("Let us find the perfect playlist for your current **mood**, based on the weather and time 🎶")

# 도시 입력
city = st.text_input("🌍 Enter your city:", placeholder="e.g., Seoul")

# 입력값 처리
if city:
    # 날씨 정보
    weather, temp = get_weather_description(city)
    if not weather:
        st.error("❌ Failed to retrieve weather data. Please check the city name.")
    else:
        # 현지 시간
        local_time = get_local_time(city)
        current_time_str = get_current_time_string(local_time)

        # 무드 분석
        mood_weather = map_weather_to_mood(weather, temp)
        mood_time = get_time_based_mood(local_time)
        combined_mood = f"{mood_weather}, {mood_time}"

        # 결과 박스
        st.markdown(f"""
        <div style="background-color:#f0f4f8; padding: 15px 20px; border-radius: 12px; margin-top: 20px; font-size:16px;">
            <b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C <br>
            <b>🕒 Local Time:</b> {current_time_str} <br>
            <b>🎯 Mood:</b> {mood_weather}, {mood_time}
        </div>
        """, unsafe_allow_html=True)

        # 추천 플레이리스트 출력
        st.subheader("🎵 Recommended Playlists:")
        playlists = search_playlist_by_mood(combined_mood)

        if playlists:
            for name, url in playlists:
                st.markdown(f"""
                <div style="background-color:#ffffff; padding:15px 20px; margin:10px 0; border-radius:10px;
                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); font-size:16px;">
                    <a href="{url}" target="_blank" style="text-decoration: none; color: #000000;">🎧 {name}</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No playlists found for your mood. Try a different city!")

        else:
            st.warning("⚠️ No playlists found for your mood.")

