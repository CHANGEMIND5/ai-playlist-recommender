from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

def get_local_time(city_name):
    try:
        geolocator = Nominatim(user_agent="playlist-recommender")
        location = geolocator.geocode(city_name)
        if not location:
            raise ValueError("City not found")

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)

        if not timezone_str:
            raise ValueError("Timezone not found")

        local_time = datetime.now(pytz.timezone(timezone_str))
        return local_time

    except Exception as e:
        print(f"❌ Error getting local time for {city_name}: {e}")
        return None

def get_time_based_mood(local_time):
    if not local_time:
        return "neutral, chill"

    hour = local_time.hour

    if hour < 6:
        return "sleepy, ambient, lofi"
    elif hour < 12:
        return "morning, fresh, upbeat"
    elif hour < 18:
        return "energetic, focus, productive"
    else:
        return "relax, calm, night, chill"

def get_current_time_string(local_time):
    if not local_time:
        return "Unknown"
    return local_time.strftime("%H:%M")


