from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from modules.config import load_config
from modules.weather import get_rain_chance

font_big = ImageFont.truetype("fonts/MonospaceBold.ttf",28)
font_medium = ImageFont.truetype("fonts/Monospace.ttf",20)
font_bold = ImageFont.truetype("fonts/MonospaceBold.ttf",20)
font_bold_bigger = ImageFont.truetype("fonts/MonospaceBold.ttf",24)
font_small = ImageFont.truetype("fonts/Monospace.ttf", 12)
font_calendar = ImageFont.truetype("fonts/MonospaceBold.ttf", 15)




def render_dashboard(weather, transport, calendar, rain):
    config = load_config()
    width = config["display"]["width"]
    height = config["display"]["height"]
    img = Image.new("1", (width, height), 255)

    draw = ImageDraw.Draw(img)

    padding = 10
    y=padding

    column = width//2

    # outline
    margin = 1
    draw.line((0,margin,width,margin), fill=0, width = 4)
    draw.line((0,height-(2.5*margin),width,height-(2.5*margin)), fill=0, width = 4)
    draw.line((margin,0,margin,height), fill=0, width = 4)
    draw.line((width-(2.5*margin),0,width-(2.5*margin),height), fill=0, width = 4)

    # header
    draw.text((padding,y), datetime.now().strftime("%A, %d %B"), font=font_big, fill=0)
    draw.text((width-(10*padding),y), datetime.now().strftime("%H:%M"), font=font_big, fill=0)
    y+=40
    draw.line((0,y,width,y), fill=0, width = 2)

    # column divider
    draw.line((column,y,column,height), fill=0, width = 3)
    right_col_y = y

    y+=20
    # left column:
    # Weather    

# main temperature
    x = padding
    x = draw_text_get_width(draw, x, y, f"{round(weather['temp'])}°C", font_bold_bigger)
    x = draw_text_get_width(draw, x+10, y+5, weather['description'], font_medium)
    
    y += 30
    
# high and low temperatures
    x = padding
    x = draw_text_get_width(draw, x, y+3, "H: ", font_medium)
    x = draw_text_get_width(draw, x-10, y, f"{weather['temp_max']}°C", font_bold_bigger)
    x = draw_text_get_width(draw, x+30, y+3, "L: ", font_medium)
    x = draw_text_get_width(draw, x-10, y, f"{weather['temp_min']}°C", font_bold_bigger)

    y += 25
    # y += 30
# sunrise & sunset
    x = padding
    x = draw_text_get_width(draw, x, y+3, "Sunrise: ", font_medium)
    x = draw_text_get_width(draw, x-10, y, f"{weather['sunrise']}", font_bold_bigger)
    x = draw_text_get_width(draw, x+30, y+3, "Sunset: ", font_medium)
    x = draw_text_get_width(draw, x-10, y, f"{weather['sunset']}", font_bold_bigger)

    y+=30

# end weather
    draw.line((0,y,column,y), fill=0, width=2)
    y+=10


# Luas data
    draw.text((padding,y), f"LUAS ~ {transport['stop']}", font=font_big, fill=0)
    y +=30
    draw.text((padding, y), "Inbound:", font=font_medium, fill=0)
    y += 25

    for tram in transport["inbound"][:2]:
        draw.text((10,y), f"→ {tram['destination']}  -  {tram['due']} min", font=font_medium, fill=0)
        y += 25
    y += 10
    draw.line((0,y,column,y), fill=0, width=2)
    y+= 10
# Rain Graph
    draw.text((padding, y), "Rain Forecast", font=font_bold, fill=0)
    y += 20
    graph_height = 120
    draw_rain_graph(draw, padding, y + 20, column - padding*2, graph_height, rain['hourly'])


# Calendar
    right_x = column+padding
    draw.text((right_x, right_col_y), "Calendar: ", font = font_big, fill = 0)
    right_col_y+=30
    for event in calendar["events"]:
        draw.text((right_x,right_col_y), f"{event['summary']}", font=font_calendar, fill=0)
        right_col_y+=20
        draw.text((right_x,right_col_y), f"{event['startTime']}  -  {event['endTime']}", font=font_medium, fill=0)
        right_col_y+=40

    return img


    # # after x=400 i want to have some nudges - "its cold! wear a coat" etc. maybe a small figure guy...





    # return img

def draw_rain_graph(draw, x, y, width, height, hourly_data):
    x, y, width, height = int(x), int(y), int(width), int(height)
    
    if not hourly_data:
        draw.text((x, y), "No forecast data", font=font_medium, fill=0)
        return
    
    # Draw scale on left side

    draw.text((x, y + height - 10), "0%", font=font_small, fill=0)
    
    # Offset bars to make room for scale
    graph_x = x + 30
    graph_width = width - 40
    
    draw.text((x, y), "100%", font=font_small, fill=0)
    for dash_x in range(graph_x, graph_x + graph_width, 10):
        draw.line((dash_x, y, dash_x + 5, y), fill=0, width=1)
    
    #50% 
    mid_y = y + height // 2
    for dash_x in range(graph_x, graph_x + graph_width, 10):
        draw.line((dash_x, mid_y, dash_x + 5, mid_y), fill=0, width=1)
    draw.text((x, mid_y - 5), "50%", font=font_small, fill=0)

    # 25%
    quarter_y = y + (height * 3 // 4)
    for dash_x in range(graph_x, graph_x + graph_width, 10):
        draw.line((dash_x, quarter_y, dash_x + 5, quarter_y), fill=0, width=1)
    draw.text((x, quarter_y - 5), "25%", font=font_small, fill=0)
    # 75%
    threequarter_y = y + (height // 4) 
    for dash_x in range(graph_x, graph_x + graph_width, 10):
        draw.line((dash_x, threequarter_y, dash_x + 5, threequarter_y), fill=0, width=1)
    draw.text((x, threequarter_y - 5), "75%", font=font_small, fill=0)
 

    draw.line((graph_x, y, graph_x, y + height), fill=0, width=1)
    draw.line((graph_x, y + height, graph_x + graph_width, y + height), fill=0, width=1)


    line_points = []
    if len(hourly_data) > 1:
        spacing = graph_width // (len(hourly_data) - 1)
    else:
        spacing = graph_width

    for i, entry in enumerate(hourly_data):
        point_x = graph_x + (i * spacing)
        point_y = y + height - int((entry["pop"] / 100) *height)
        line_points.append((point_x, point_y))
        draw.text((point_x, y + height + 5), entry["hour"][:2], font=font_small, fill=0)
        draw.ellipse((point_x - 3, point_y - 3, point_x + 3, point_y + 3), fill=0)


    if len(line_points)>1:
        draw.line(line_points, fill=0, width=3)



def draw_text_get_width(draw, x, y, text, font):
    draw.text((x, y), text, font=font, fill=0)
    bbox = draw.textbbox((x, y), text, font=font)
    return bbox[2]