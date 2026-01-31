from modules.weather import get_weather
from modules.transport import get_luas_arrivals
from modules.calendar import get_todays_events
from renderer.layout import render_dashboard



weather = get_weather()
transport = get_luas_arrivals("GAL")
calendar = get_todays_events()



img = render_dashboard(weather,transport, calendar)

img.save("dashboard.png")