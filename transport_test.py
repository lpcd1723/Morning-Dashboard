import requests
import xml.etree.ElementTree as ET

def get_luas_arrivals(stop_name):
    url = f"https://luasforecasts.rpa.ie/xml/get.ashx?action=forecast&stop={stop_name}&encrypt=false"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # arrival = r
            return response.text
        else:
            print("Error", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error", e)
        return None

def main():
    STOP = "GAL"
    arrivals = get_luas_arrivals(STOP)
    if arrivals:
        root = ET.fromstring(arrivals)
        print(root.attrib["stop"])
        directions = root.findall("direction")

        for direction in directions:
            print(direction.attrib["name"])
            trams = direction.findall("tram")

            for tram in trams[:3]:
                print("Due in:",tram.attrib["dueMins"],"minute(s)", "Destination:", tram.attrib["destination"])

    else:
        print("Failed to fetch posts from API.")

if __name__ == '__main__':
    main()