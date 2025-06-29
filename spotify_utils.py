import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_playlist_by_mood(mood_keyword):
    try:
        print(f"🔍 Searching Spotify for keyword: {mood_keyword}")
        results = sp.search(q=mood_keyword, type='playlist', limit=5)
        playlists = []

        for item in results['playlists']['items']:
            playlist_name = item['name']
            playlist_url = item['external_urls']['spotify']
            image_url = item['images'][0]['url'] if item['images'] else "https://via.placeholder.com/80"

            playlists.append({
                "name": playlist_name,
                "url": playlist_url,
                "image_url": image_url
            })

        print(f"✅ Found {len(playlists)} playlists for: {mood_keyword}")
        return playlists

    except Exception as e:
        print(f"❌ Spotify search error: {e}")
        return []

        return [("Focus Flow", "https://open.spotify.com/playlist/37i9dQZF1DXc2aPBXGmXrt")]
