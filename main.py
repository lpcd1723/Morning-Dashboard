from modules.weather import get_weather, get_rain_chance
from modules.transport import get_luas_arrivals
from modules.calendar import get_todays_events
from renderer.layout import render_dashboard
from modules.config import load_config
import time
from datetime import datetime
def main():  
    config = load_config()
    refresh_interval = config["display"]["refresh_interval"]
    while True:
        stop = config["transport"]["stop"]
        weather = get_weather()
        transport = get_luas_arrivals(stop)
        calendar = get_todays_events()
        rain = get_rain_chance()


        img = render_dashboard(weather,transport, calendar, rain)

        img.save("dashboard.png")
        print(f"Dashboard updated at {datetime.now().strftime('%H:%M:%S')}")

        time.sleep(refresh_interval)

if __name__ == "__main__":
    main()