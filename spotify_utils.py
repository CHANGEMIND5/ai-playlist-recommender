import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

# Validate credentials
if not client_id or not client_secret:
    raise ValueError(
        "Spotify client credentials not found. Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in your environment."
    )

# Initialize Spotipy client
auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=auth_manager)

def search_playlist_by_mood(mood_keyword):
    """
    Search for playlists matching the mood keyword.
    Returns a list of dicts with name, url, and image_url.
    """
    print(f"🔍 Searching Spotify for keyword: {mood_keyword}")
    try:
        results = sp.search(q=mood_keyword, type="playlist", limit=5)
        items = results.get("playlists", {}).get("items", [])
        playlists = []

        for item in items:
            name = item.get("name")
            url = item.get("external_urls", {}).get("spotify")
            images = item.get("images") or []
            image_url = images[0].get("url") if images else "https://via.placeholder.com/80"

            playlists.append({
                "name": name,
                "url": url,
                "image_url": image_url
            })

        print(f"✅ Found {len(playlists)} playlists for: {mood_keyword}")
        return playlists

    except SpotifyOauthError as e:
        print(f"❌ Spotify OAuth error: {e}")
        return []
    except Exception as e:
        print(f"❌ Spotify search error: {e}")
        return []
