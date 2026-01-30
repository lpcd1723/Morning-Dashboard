import requests
import json 
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

lat = 53.3498
lon = -6.2603

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
            return weather
        else:
            print("Error", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None
    
def main():
    weather = get_weather()
    if weather:

        temp = weather["main"]["temp"]
        temp_max = weather["main"]["temp_max"]
        temp_min = weather["main"]["temp_min"]
        description = weather["weather"][0]["description"]

        sunrise = weather["sys"]["sunrise"]
        sunset = weather["sys"]["sunset"]

        sunrise = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(sunrise))
        sunset = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(sunset))

        print(f"Current Temperature: {temp}°C")
        print(f"High: {temp_max}°C, Low: {temp_min}°C")
        print(f"Conditions: {description}")
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")

    else:
        print("Failed to fetch posts from API.")
    
if __name__ == '__main__':
    main()

