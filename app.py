import streamlit as st
from weather_utils import get_weather_description, map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string

# Streamlit 타이틀
st.title("🎵 AI Music Playlist Recommender")

# 사용자 입력
city = st.text_input("🌍 Enter your city:")

if city:
    # 1. 날씨 정보 가져오기
    weather, temp = get_weather_description(city)
    if not weather:
        st.error("❌ Failed to retrieve weather data. Please check the city name or try again.")
    else:
        st.write(f"🌤️ Weather: {weather}, 🌡️ Temp: {temp}°C")

        # 2. 도시 기반 현지 시간 가져오기
        local_time = get_local_time(city)
        current_time_str = get_current_time_string(local_time)

        # 3. 무드 결정 (날씨 기반 + 시간 기반)
        mood_weather = map_weather_to_mood(weather, temp)
        mood_time = get_time_based_mood(local_time)

        # 4. 출력
        st.write(f"🕒 Current Time in {city}: {current_time_str}")
        st.write(f"🎯 Mood by weather: {mood_weather} / by time: {mood_time}")

        # 5. 추천 플레이리스트 검색
        combined_mood = f"{mood_weather}, {mood_time}"
        playlists = search_playlist_by_mood(combined_mood)

        if playlists:
            st.subheader("🎵 Recommended Playlists:")
            for name, url in playlists:
                st.markdown(f"- [{name}]({url})")
        else:
            st.warning("⚠️ No playlists found for your mood.")

