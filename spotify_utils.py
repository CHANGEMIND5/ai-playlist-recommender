import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st  # ✅ secrets 불러오기 위해 필요

# Authenticate with Spotify API using secrets
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=st.secrets["SPOTIFY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]
))

def search_playlist_by_mood(mood_keywords):
    try:
        keywords = [kw.strip().lower() for kw in mood_keywords.split(",") if kw.strip()]

        for keyword in keywords:
            print(f"🔍 Searching Spotify for keyword: {keyword}")
            results = sp.search(q=keyword, type='playlist', limit=5)
            print("🔎 Raw Spotify result:", results)

            if not results or "playlists" not in results:
                continue

            playlists_data = results.get("playlists")
            if not playlists_data or "items" not in playlists_data:
                continue

            items = playlists_data["items"]

            # ✅ None이 아닌 아이템만 필터링
            valid_items = [item for item in items if item is not None]

            if valid_items:
                playlists = [
                    (item["name"], item["external_urls"]["spotify"])
                    for item in valid_items
                ]
                if playlists:
                    print(f"✅ Found playlists for: {keyword}")
                    return playlists

        print("⚠️ No playlists found. Using fallback.")
        return [("Focus Flow", "https://open.spotify.com/playlist/37i9dQZF1DXc2aPBXGmXrt")]

    except Exception as e:
        print(f"❌ Spotify API error: {e}")
        return [("Focus Flow", "https://open.spotify.com/playlist/37i9dQZF1DXc2aPBXGmXrt")]
