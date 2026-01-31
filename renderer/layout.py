from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

font_big = ImageFont.truetype("fonts/MonospaceBold.ttf",28)
font_medium = ImageFont.truetype("fonts/Monospace.ttf",20)
font_bold = ImageFont.truetype("fonts/MonospaceBold.ttf",20)

def render_dashboard(weather, transport, calendar):
    img = Image.new("1", (800, 480), 255)

    draw = ImageDraw.Draw(img)

    draw.text((10,10), datetime.now().strftime("%A, %d %B"), font=font_big, fill=0)
    draw.text((700,10), datetime.now().strftime("%H:%M"), font=font_big, fill=0)

    draw.line((0,50,800,50), fill=0, width=2)

    # Weather

    draw.text((10,70), f"{weather['temp']}°C", font=font_medium, fill=0)
    draw.text((100,70), f"{weather['description']}", font=font_medium, fill=0)

    draw.text((10,100), f"High: {weather['temp_max']}°C", font=font_medium, fill=0)
    draw.text((200,100), f"Low: {weather['temp_min']}°C", font=font_medium, fill=0)

    draw.text((10,130), f"Sunrise: {weather['sunrise']}", font=font_medium, fill=0)
    draw.text((200,130), f"Sunset: {weather['sunset']}", font=font_medium, fill=0)

    # after x=400 i want to have some nudges - "its cold! wear a coat" etc. maybe a small figure guy...
    draw.line((0,170,800,170), fill=0, width=2)

    # Luas data

    draw.text((10,175), f"LUAS ~ {transport['stop']}", font=font_big, fill=0)
    y = 210
    draw.text((10,y), "Inbound:", font=font_medium, fill=0)
    y += 25

    for tram in transport["inbound"][:3]:
        draw.text((10,y), f"→ {tram['destination']}  -  {tram['due']} min", font=font_medium, fill=0)
        y += 25


    draw.line((0,310,800,310), fill=0, width=2)

    # Calendar
    y = 330
    for event in calendar["events"]:
        draw.text((10,y), f"{event['summary']}", font=font_bold, fill=0)
        y+=20
        draw.text((10,y), f"{event['startTime']}  -  {event['endTime']}", font=font_medium, fill=0)
        y+=40

    return img
# def main():
#     weather = {
#         "temp": 9.14,
#         "temp_max": 10.51,
#         "temp_min": 8.25,
#         "description": "scattered clouds",
#         "sunrise": "08:12",
#         "sunset": "17:34"
#     }
#     transport = {
#         "stop": "The Gallops",
#         "inbound": [
#             {"destination": "Parnell", "due": "3"},
#             {"destination": "Parnell", "due": "14"},
#             {"destination": "Parnell", "due": "25"}
#         ],
#         "outbound": [
#             {"destination": "Brides Glen", "due": "7"},
#             {"destination": "Brides Glen", "due": "19"},
#             {"destination": "Brides Glen", "due": "23"}

#         ]
#     }
#     calendar = {
#         "eventNumber": 1,
#         "events": [
#             {"summary": "Software Engineering", "startTime": "10:00", "endTime": "11:00", "location": "Lonsdale Bldg"},
#             {"summary": "Computing II", "startTime": "12:00", "endTime": "14:00", "location": ""}
#         ]
#     }
#     img = render_dashboard(weather, transport,calendar)
#     img.save("dashboard.png")
# if __name__ == "__main__":
#     main()
