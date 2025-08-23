# Weather Report App 

This is a simple command-line Python app that fetches real-time weather information for any U.S. city using the OpenWeather API.

## Features

- Takes user input for a city
- Shows temperature in Celsius
- Shows humidity
- Shows a short description of the weather

## How to Run

1. Clone this repo
2. Create a `.env` file in the same folder and add:

OPENWEATHER_API_KEY=your_actual_api_key_here

3. (Optional) Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate


4. Run the app:

bash
Copy
Edit
python3 get_weather.py


# Current Weather Now — Streamlit App

A minimal Streamlit app that fetches **current weather** for a city using the **OpenWeatherMap** API.

## Features
- Streamlit text input for the **city** (user input requirement ✅)
- Calls the **OpenWeatherMap** weather API (requests + `OPENWEATHER_API_KEY`) ✅
- Displays temp (°C/°F), feels-like, humidity, wind, and an emoji-tailored description ✅
- Optional map pinned to the city’s coordinates ✅
- Clean error handling for invalid city names ✅

---

## Local Setup (Recommended)
1. **Clone** this folder or copy the files into your project.
2. Create a virtual env and install deps:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root (same folder as `app.py`) and add your API key:
   ```bash
   cp .env.example .env
   # then edit .env and paste your key
   OPENWEATHER_API_KEY=your_openweather_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
5. Open the URL that Streamlit prints (typically `http://localhost:8501`).  

---

## How It Works
- `app.py` uses `dotenv` to read `OPENWEATHER_API_KEY` from `.env`.
- It hits `https://api.openweathermap.org/data/2.5/weather?q=<city>&appid=<KEY>&units=metric`.
- Results are cached for 5 minutes with `@st.cache_data`.
- You can toggle °C/°F in the sidebar.

---

## Make it Your Own (ideas)
- Add a 5‑day forecast chart (use the `/forecast` API).
- Add custom icons or background images.
- Log recent searches in `st.session_state`.

---

