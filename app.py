import requests
import os
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(API_KEY)


def get_weather(city):
    """
    Fetch weather for the given city and print it nicely.
    """
    # 1. Create the API endpoint URL
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # 2. Set query parameters
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # temperature in Celsius
    }
    
    # 3. Make the request
    response = requests.get(url, params=params)
    
    # 4. Parse JSON
    data = response.json()

    #avoid error if city not found
    if response.status_code != 200:
        print("⚠️ Error:", data.get("message", "Unknown error"))
        return
    
    # 5. Extract key info
    city_name = data["name"]
    temp_c = data["main"]["temp"]
    temp_f = (temp_c * 9/5) + 32
    description = data["weather"][0]["description"]
    #extract humidity
    humidity = data["main"]["humidity"]
    
    # 6. Print
    print(f"In {city_name}, it is {temp_c}°C / {temp_f}°F with {description} and and humidity of {humidity}.")


# get_weather.py  (replace your file with this)

import os
import requests
from dotenv import load_dotenv

# --- Optional: Streamlit UI (only used when launched via `streamlit run`) ---
try:
    import streamlit as st # type: ignore
    _HAS_STREAMLIT = True
except Exception:
    _HAS_STREAMLIT = False

# Load your API key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def _c_to_f(c):
    return c * 9 / 5 + 32


def get_weather(city: str):
    """
    Fetch weather for the given city.
    Returns (status_code, data_dict) where data_dict is the parsed JSON.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}  # metric = Celsius
    resp = requests.get(url, params=params, timeout=20)
    data = resp.json()
    return resp.status_code, data


# ------------------------ STREAMLIT APP ------------------------
def run_streamlit_app():
    st.set_page_config(page_title="Weather Now", page_icon="⛅", layout="centered")
    st.title("Current Weather ")
    st.caption("Enter a city and get the current weather from OpenWeatherMap.")

    if not API_KEY:
        st.warning(
            "No API key found in **OPENWEATHER_API_KEY**. "
            "Create a `.env` file with `OPENWEATHER_API_KEY=your_key` then restart.",
            icon="⚠️",
        )

    with st.sidebar:
        st.header("Settings")
        units = st.radio("Temperature units", ["Celsius (°C)", "Fahrenheit (°F)"], index=0)

    city = st.text_input("City", placeholder="e.g., Durham, New York, London")
    go = st.button("Get Weather", type="primary")

    if go and city.strip():
        status, data = get_weather(city.strip())
        if status != 200:
            st.error(f"Could not fetch weather for **{city}** — {data.get('message','Unknown error').capitalize()}")
            return

        name = data.get("name", city.title())
        main = data.get("main", {})
        weather_list = data.get("weather", [{}])
        wind = data.get("wind", {})
        coord = data.get("coord", {})

        temp_c = main.get("temp")
        feels_c = main.get("feels_like")
        humidity = main.get("humidity")
        desc = weather_list[0].get("description", "n/a").capitalize()

        if units.startswith("Fahrenheit"):
            temp_display = f"{_c_to_f(temp_c):.1f} °F" if temp_c is not None else "n/a"
            feels_display = f"{_c_to_f(feels_c):.1f} °F" if feels_c is not None else "n/a"
        else:
            temp_display = f"{temp_c:.1f} °C" if temp_c is not None else "n/a"
            feels_display = f"{feels_c:.1f} °C" if feels_c is not None else "n/a"

        # simple emoji
        dlow = desc.lower()
        if "thunder" in dlow: emoji = "⛈️"
        elif "rain" in dlow or "drizzle" in dlow: emoji = "🌧️"
        elif "snow" in dlow: emoji = "❄️"
        elif "cloud" in dlow: emoji = "☁️"
        elif "clear" in dlow: emoji = "☀️"
        elif any(x in dlow for x in ["mist", "fog", "haze"]): emoji = "🌫️"
        else: emoji = "🌈"

        st.subheader(f"{emoji}  {name}")
        st.write(desc)

        c1, c2, c3 = st.columns(3)
        c1.metric("Temperature", temp_display)
        c2.metric("Feels like", feels_display)
        c3.metric("Humidity", f"{humidity}%")

        st.write(f"**Wind:** {wind.get('speed','n/a')} m/s, {wind.get('deg','n/a')}°")
        if isinstance(coord, dict) and "lat" in coord and "lon" in coord:
            # lightweight map (works without extra libs)
            st.map({"lat": [coord["lat"]], "lon": [coord["lon"]]})


# ------------------------ CLI FALLBACK ------------------------
def run_cli():
    city = input("Enter a city name: ").strip()
    status, data = get_weather(city)
    if status != 200:
        print("⚠️ Error:", data.get("message", "Unknown error"))
        return
    name = data["name"]
    temp_c = data["main"]["temp"]
    temp_f = _c_to_f(temp_c)
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    print(f"In {name}, it is {temp_c:.1f}°C / {temp_f:.1f}°F with {desc} and humidity of {humidity}%.")


if __name__ == "__main__":
    # Streamlit takes over when you run with `streamlit run`
    if _HAS_STREAMLIT:
        run_streamlit_app()
    else:
        run_cli()


