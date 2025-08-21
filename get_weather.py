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

# accept user input 
city = input("Enter a city name: ")
get_weather(city)



#extract temp in celsius

# extract description of weather

