import streamlit as st
import requests
from weather_utils import map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string
from gemini_utils import generate_mood

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
    if feeling.strip() == "":
        st.warning("😊 Please enter a valid feeling to get personalized recommendations.")
    else:
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

            if local_time is None:
                st.warning("⚠️ Unable to retrieve local time. Displaying 'Unknown' and using default mood.")

            current_time_str = get_current_time_string(local_time)
            mood_weather = map_weather_to_mood(weather, temp)
            mood_time = get_time_based_mood(local_time)

            with st.spinner("🔮 Generating mood with Gemini..."):
                combined_mood = generate_mood(feeling, city)

            if combined_mood.lower() == "calm reflective mood":
                st.warning("⚠️ Gemini did not return a mood. Using weather-based mood instead.")
                combined_mood = f"{mood_weather}, {mood_time}"

            info_html = f"""
            <div style="background-color:#f0f4f8; padding: 15px 20px; border-radius: 12px; margin-top: 20px; font-size:16px;">
            <b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C <br>
            <b>🕒 Local Time in {city}:</b> {current_time_str} <br>
            <b>🎯 Mood (Weather/Time):</b> {mood_weather}, {mood_time} <br>
            <b>✨ Gemini Extracted Mood:</b> {combined_mood}
            </div>
            """
            st.markdown(info_html, unsafe_allow_html=True)

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
                st.warning("⚠️ No playlists found for your mood. Try a different city or feeling!")

elif city and not feeling:
    st.info("😊 Please enter your current feeling to get personalized mood recommendations.")
else:
    st.info("🌍 Please enter a city and your feeling to get your mood-based playlist recommendations.")
