import streamlit as st
import requests
import re
from weather_utils import map_weather_to_mood
from spotify_utils import search_playlist_by_mood
from time_utils import get_local_time, get_time_based_mood, get_current_time_string
from openai_utils import generate_mood

# --- Theme Toggle ---
theme = st.radio("Select Theme", ("Light", "Dark"), index=1)
if theme == "Dark":
    bg_color = "rgba(30,30,30,0.6)"
    text_color = "#ddd"
    card_bg = "rgba(50,50,50,0.8)"
else:
    bg_color = "#ffffff"
    text_color = "#000"
    card_bg = "#f9f9f9"

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
        # Time retrieval with caching
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

        # Generate mood with OpenAI
        with st.spinner("🔮 Generating mood with OpenAI..."):
            combined_mood = generate_mood(feeling, weather, temp, mood_time)
        if combined_mood.lower() == "calm reflective mood":
            st.warning("⚠️ OpenAI did not return a mood. Using weather-based mood instead.")
            combined_mood = f"{mood_weather}, {mood_time}"

        # Share/Clipboard button
        share_col, _ = st.columns([1,3])
        with share_col:
            if st.button("Copy Mood"):
                st.write(f"📝 Mood: {combined_mood} (copy above)")

        # Info Card with icons and mood tag highlight
        info_html = f"""
        <div style="background-color:{bg_color}; padding: 20px; border-radius: 12px; margin-top: 20px; color:{text_color};">
          <p style="margin:0;"><b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C</p>
          <p style="margin:0;"><b>🕒 Time:</b> {mood_time} ({current_time_str})</p>
          <p style="margin-top:10px;"><b>✨ Mood:</b> <span style="background:#4b4b4b;color:#fff;padding:4px 8px;border-radius:4px;">{combined_mood}</span></p>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

        # Refine search key: punctuation removed, top 3 words
        clean = re.sub(r'[^A-Za-z0-9 ]', '', combined_mood)
        tokens = clean.split()
        search_key = " ".join(tokens[:3]) if tokens else combined_mood

        # Playlist Grid
        st.subheader("🎵 Recommended Playlists:")
        playlists = search_playlist_by_mood(search_key)
        if playlists:
            cols = st.columns(2)
            for idx, playlist in enumerate(playlists):
                with cols[idx % 2]:
                    name = playlist.get("name")
                    url = playlist.get("url")
                    image_url = playlist.get("image_url")
                    card_html = f"""
                    <div style="background-color:{card_bg}; padding:15px; margin:10px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                      <img src="{image_url}" style="width:100%; border-radius:8px;">
                      <a href="{url}" target="_blank" style="text-decoration:none;color:{text_color};font-weight:bold;">🎧 {name}</a>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No playlists found. Try a different mood!")

elif city and not feeling:
    st.info("😊 Please enter your current feeling to get personalized mood recommendations.")
else:
    st.info("🌍 Please enter a city and your feeling to get your mood-based playlist recommendations.")



