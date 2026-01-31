import requests
import xml.etree.ElementTree as ET

def get_luas_arrivals(stop_name):
    url = f"https://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop={stop_name}&encrypt=false"
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
            
            return {
                "stop":stop,
                "inbound":inbound,
                "outbound":outbound
            }
        
        else:
            print("Error", response.status_code)
            return None
    
    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None
