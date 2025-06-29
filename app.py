import streamlit as st
import requests
import re
from weather_utils import map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string
from openai_utils import generate_mood

st.set_page_config(
    page_title="Skytonees",
    page_icon="🎧",
    layout="centered"
)

st.title("🎵 Skytonees: AI Music Playlist Recommender")
st.markdown(
    "Let us find the perfect playlist for your **mood**, based on the weather, time, and your feeling 🎶"
)

city = st.text_input("🌍 Enter your city:", placeholder="e.g., Seoul").strip()
feeling = st.text_input("😊 How do you feel now?", placeholder="e.g., Happy, Tired, Excited").strip()

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

if city and feeling:
    weather, temp = get_weather_description(city)

    if weather is None or temp is None:
        st.error("❌ Failed to retrieve weather data. Please check the city name.")
    else:
        if 'city_cache' not in st.session_state:
            st.session_state.city_cache = {}

        if city in st.session_state.city_cache:
            local_time = st.session_state.city_cache[city]
        else:
            local_time = get_local_time(city)
            st.session_state.city_cache[city] = local_time

        current_time_str = get_current_time_string(local_time)
        mood_weather = map_weather_to_mood(weather, temp)
        mood_time = get_time_based_mood(local_time)

        with st.spinner("🔮 Generating mood with OpenAI..."):
            combined_mood = generate_mood(feeling, weather, temp, mood_time)

        if combined_mood.lower() == "calm reflective mood":
            st.warning("⚠️ OpenAI did not return a mood. Using weather-based mood instead.")
            combined_mood = f"{mood_weather}, {mood_time}"

        # 키워드 정제: 특수문자 제거, 상위 3단어만 사용하여 검색
        clean_mood = re.sub(r'[^A-Za-z0-9 ]', '', combined_mood)
        tokens = clean_mood.split()
        search_key = " ".join(tokens[:3]) if tokens else combined_mood
        print(f"🔍 Refined search key: {search_key}")
        playlists = search_playlist_by_mood(search_key)

        info_html = f"""
        <div style="background-color: rgba(30,30,30,0.6); padding: 15px 20px; border-radius: 12px; margin-top: 20px; font-size:16px; color:#ddd;">
        <b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C <br>
        <b>🕒 Local Time in {city}:</b> {current_time_str} <br>
        <b>🎯 Mood (Weather/Time):</b> {mood_weather}, {mood_time} <br>
        <b>✨ OpenAI Extracted Mood:</b> {combined_mood}
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

        st.subheader("🎵 Recommended Playlists:")
        if playlists:
            for playlist in playlists:
                name = playlist.get("name")
                url = playlist.get("url")
                image_url = playlist.get("image_url")

                card_html = f"""
                <div style="background-color: rgba(30,30,30,0.6); padding:15px 20px; margin:10px 0; border-radius:10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4); font-size:16px; color: #dddddd; display: flex; align-items: center;">
                    <img src="{image_url}" alt="playlist cover" style="width:80px; height:80px; border-radius:8px; margin-right:15px;">
                    <a href="{url}" target="_blank" style="text-decoration: none; color: #ffffff; font-weight: bold;">🎧 {name}</a>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No playlists found for your mood. Try a different city or feeling!")

elif city and not feeling:
    st.info("😊 Please enter your current feeling to get personalized mood recommendations.")
else:
    st.info("🌍 Please enter a city and your feeling to get your mood-based playlist recommendations.")


