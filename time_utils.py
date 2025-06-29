from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import time

def get_local_time(city_name):
    """
    도시 이름을 받아 현지 시간을 반환.
    실패 시 None 반환.
    """
    try:
        # Rate limit 방지용 딜레이
        time.sleep(1)

        geolocator = Nominatim(user_agent="skytonees-app")
        location = geolocator.geocode(city_name, timeout=10)

        if not location:
            print(f"❌ Geolocation failed for {city_name}.")
            return None

        lat, lon = location.latitude, location.longitude
        print(f"📍 {city_name} => Coordinates: ({lat}, {lon})")

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=lat, lng=lon)

        if not timezone_str:
            print(f"❌ Timezone not found for coordinates: {lat}, {lon}.")
            return None

        timezone = pytz.timezone(timezone_str)
        local_time = datetime.now(timezone)
        print(f"⏰ Local time in {city_name}: {local_time}")

        return local_time

    except Exception as e:
        print(f"❌ Error getting local time for {city_name}: {e}")
        return None

def get_time_based_mood(local_time):
    """
    현지 시간에 따라 무드를 반환.
    실패 시 중립 무드 반환.
    """
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
    """
    현지 시간을 문자열 (HH:MM)로 반환.
    실패 시 'Unknown' 반환.
    """
    if not local_time:
        return "Unknown"
    return local_time.strftime("%H:%M")

# 직접 실행 시 테스트
if __name__ == "__main__":
    test_city = "London"
    local_time = get_local_time(test_city)
    print("🕒 Time String:", get_current_time_string(local_time))
    print("🎶 Mood:", get_time_based_mood(local_time))