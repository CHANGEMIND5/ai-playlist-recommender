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
    text_color = "#ddd"
else:
    text_color = "#000"

# --- Background Gradient Selection Function ---
def get_background_gradient(weather, time_of_day):
    w = weather.lower()
    t = time_of_day.lower()
    # Weather-based overrides
    if "rain" in w:
        return ("#4e54c8", "#8f94fb")  # blue gradient
    if "snow" in w or "sleet" in w:
        return ("#e0eafc", "#cfdef3")  # icy gradient
    if "cloud" in w:
        return ("#bdc3c7", "#2c3e50")  # grey gradient
    if "sunny" in w or "clear" in w:
        # time-based for sunny
        if t == "morning":
            return ("#FFDEE9", "#B5FFFC")
        if t == "afternoon":
            return ("#FBD786", "#f7797d")
        if t == "evening":
            return ("#FFA17F", "#00223E")
        if t == "night":
            return ("#0F2027", "#203A43")
    # Default by time of day
    if t == "morning":
        return ("#FFFAF0", "#FFD1DC")
    if t == "afternoon":
        return ("#FFF1A1", "#FFD3A5")
    if t == "evening":
        return ("#C33764", "#1D2671")
    # night
    return ("#0F2027", "#203A43")

# Page config
st.set_page_config(
    page_title="Skytonees",
    page_icon="🎧",
    layout="centered"
)

# Initial inputs
st.title("🎵 Skytonees: AI Music Playlist Recommender")
st.markdown("Let us find the perfect playlist for your **mood**, based on the weather, time, and your feeling 🎶")
city = st.text_input("🌍 Enter your city:", placeholder="e.g., Seoul").strip()
feeling = st.text_input("😊 How do you feel now?", placeholder="e.g., Happy, Tired, Excited").strip()

# Fetch weather
if city and feeling:
    weather, temp = (None, None)
    try:
        key = st.secrets["WEATHERAPI_KEY"]
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no"
        res = requests.get(url)
        data = res.json()
        weather = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
    except:
        st.error("❌ Failed to retrieve weather. Check your city name.")

    if weather and temp is not None:
        # Get local time
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

        # Background gradient
        color1, color2 = get_background_gradient(weather, mood_time)
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(to bottom right, {color1}, {color2});
                background-attachment: fixed;
            }}
            </style>
        """, unsafe_allow_html=True)

        # Generate mood
        with st.spinner("🔮 Generating mood with OpenAI..."):
            combined_mood = generate_mood(feeling, weather, temp, mood_time)
        if combined_mood.lower() == "calm reflective mood":
            st.warning("⚠️ OpenAI fallback. Using weather/time mood.")
            combined_mood = f"{mood_weather}, {mood_time}"

        # Info card
        st.markdown(f"""
            <div style="padding:20px; border-radius:12px; color:{text_color};">
              <b>🌤️ Weather:</b> {weather} &nbsp;&nbsp; <b>🌡️ Temp:</b> {temp}°C<br>
              <b>🕒 Time:</b> {mood_time} ({current_time_str})<br>
              <b>✨ Mood:</b> <span style="background:rgba(0,0,0,0.3); padding:4px 8px; border-radius:4px;">{combined_mood}</span>
            </div>
        """, unsafe_allow_html=True)

        # Refine keyword
        clean = re.sub(r'[^A-Za-z0-9 ]', '', combined_mood)
        tokens = clean.split()
        search_key = " ".join(tokens[:3]) if tokens else combined_mood

        # Playlists grid
        st.subheader("🎵 Recommended Playlists:")
        playlists = search_playlist_by_mood(search_key)
        if playlists:
            cols = st.columns(2)
            for i, p in enumerate(playlists):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div style="background:rgba(255,255,255,0.2); padding:15px; margin:10px; border-radius:10px;">
                          <img src="{p['image_url']}" style="width:100%; border-radius:8px;">
                          <a href="{p['url']}" target="_blank" style="color:{text_color}; font-weight:bold;">🎧 {p['name']}</a>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No playlists found. Try another mood!")

elif city and not feeling:
    st.info("😊 Please enter your current feeling.")
else:
    st.info("🌍 Please enter a city and your feeling.")