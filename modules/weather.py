import requests
import os
from dotenv import load_dotenv
import time
from modules.cache import get_cached_data, save_to_cache
from modules.config import load_config
from datetime import datetime


config = load_config()

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

lat = config["weather"]["lat"]
lon = config["weather"]["lon"]
cache_time = config["weather"]["cache_duration"]

def get_rain_chance():
    cached = get_cached_data("cache/forecast.json", cache_time)
    if cached:
        return cached
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            today = datetime.now().strftime("%Y-%m-%d")
            max_pop = 0
            hourly = []
            
            current_pop = hourly[0]["pop"] if hourly else 0
            current_hour = datetime.now().strftime("%H:%M")
            hourly.insert(0, {"hour": current_hour, "pop": current_pop})
            for entry in data["list"]:
                if entry["dt_txt"].startswith(today):
                    pop = entry["pop"]
                    hour = entry["dt_txt"][11:16] 
                    hourly.append({"hour":hour, "pop":round(pop *100)})
                    if pop > max_pop:
                        max_pop = pop
            
            result = {
                "rain_chance": round(max_pop * 100),
                "hourly": hourly 
            }
            save_to_cache("cache/forecast.json", result)
            return result
        else:
            return {"rain_chance": 0, "hourly":[]}
    except:
        return {"rain_chance": 0, "hourly":[]}

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    cached = get_cached_data("cache/weather.json", cache_time)
    if cached: 
        return cached
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            temp = weather["main"]["temp"]
            temp_max = weather["main"]["temp_max"]
            temp_min = weather["main"]["temp_min"]
            description = weather["weather"][0]["description"]

            sunrise = weather["sys"]["sunrise"]
            sunset = weather["sys"]["sunset"]

            sunrise = time.strftime('%H:%M', time.localtime(sunrise))
            sunset = time.strftime('%H:%M', time.localtime(sunset))
            result = {
                "temp": temp,
                "temp_max":temp_max,
                "temp_min":temp_min,
                "description":description,
                "sunrise":sunrise,
                "sunset":sunset
            }

            # save to cache
            save_to_cache("cache/weather.json", result)
            return result
        else:
            print("Error", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None
    