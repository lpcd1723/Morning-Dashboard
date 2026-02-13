import requests
import xml.etree.ElementTree as ET
from modules.cache import get_cached_data, save_to_cache
from modules.config import load_config

def get_luas_arrivals(stop_name):
    url = f"https://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop={stop_name}&encrypt=false"
    config = load_config()
    cache_time = config["transport"]["cache_duration"]
    cached = get_cached_data("cache/transport.json", cache_time)
    if cached:
        return cached
    
    try:
        response = requests.get(url)
        if response.status_code == 200:

            root = ET.fromstring(response.text)
            stop = root.attrib["stop"]
            directions = root.findall("direction")
            inbound = []
            outbound = []

            for direction in directions:
                trams = direction.findall("tram")
                for tram in trams[:3]:
                    tram_data = {
                        "destination":tram.attrib["destination"],
                        "due":tram.attrib["dueMins"]
                    }
                    if direction.attrib["name"] == "Inbound":
                        inbound.append(tram_data)
                    else:
                        outbound.append(tram_data)
            data = {
                "stop":stop,
                "inbound":inbound,
                "outbound":outbound
            }
            save_to_cache("cache/transport.json", data)
            return data
        
        else:
            print("Error", response.status_code)
            return None
    
    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None
