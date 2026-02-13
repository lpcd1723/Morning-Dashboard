from modules.weather import get_weather, get_rain_chance
from modules.transport import get_luas_arrivals
from modules.calendar import get_todays_events
from renderer.layout import render_dashboard
from modules.config import load_config
def main():  
    config = load_config()
    stop = config["transport"]["stop"]
    weather = get_weather()
    transport = get_luas_arrivals(stop)
    calendar = get_todays_events()
    rain = get_rain_chance()


    img = render_dashboard(weather,transport, calendar, rain)

    img.save("dashboard.png")

if __name__ == "__main__":
    main()