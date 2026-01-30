"""
Weather module - Fetches weather data from OpenWeatherMap or Met Éireann
"""
import requests
from datetime import datetime, timedelta
import json
import os
import yaml
        


# class WeatherProvider:
#     def __init__(self, config, cache_dir="cache"):
#         self.config = config
#         self.cache_dir = cache_dir
#         self.cache_file = os.path.join(cache_dir, "weather_cache.json")
        
#     def get_weather(self):
#         """Get weather data, using cache if available and fresh"""
#         # Check cache first
#         cached_data = self._load_cache()
#         if cached_data:
#             return cached_data
            
#         # Fetch fresh data
#         if self.config['weather']['provider'] == 'openweathermap':
#             data = self._fetch_openweathermap()
#         else:
#             data = self._fetch_met_eireann()
            
#         # Save to cache
#         self._save_cache(data)
#         return data
    
#     def _fetch_openweathermap(self):
#         """Fetch from OpenWeatherMap API"""
#         api_key = self.config['weather']['api_key']
#         lat = self.config['location']['lat']
#         lon = self.config['location']['lon']
        
#         # Current weather
#         current_url = "https://api.openweathermap.org/data/2.5/weather"
#         params = {
#             'lat': lat,
#             'lon': lon,
#             'appid': api_key,
#             'units': 'metric'
#         }
        
#         try:
#             response = requests.get(current_url, params=params, timeout=10)
#             response.raise_for_status()
#             current = response.json()
            
#             # Forecast for high/low
#             forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
#             forecast_response = requests.get(forecast_url, params=params, timeout=10)
#             forecast_response.raise_for_status()
#             forecast = forecast_response.json()
            
#             # Process forecast for today's high/low
#             today = datetime.now().date()
#             today_temps = []
#             rain_chance = 0
            
#             for item in forecast['list']:
#                 item_date = datetime.fromtimestamp(item['dt']).date()
#                 if item_date == today:
#                     today_temps.append(item['main']['temp'])
#                     if 'rain' in item:
#                         rain_chance = max(rain_chance, item.get('pop', 0) * 100)
            
#             return {
#                 'current_temp': round(current['main']['temp']),
#                 'high': round(max(today_temps)) if today_temps else round(current['main']['temp_max']),
#                 'low': round(min(today_temps)) if today_temps else round(current['main']['temp_min']),
#                 'rain_chance': round(rain_chance),
#                 'description': current['weather'][0]['description'],
#                 'sunrise': datetime.fromtimestamp(current['sys']['sunrise']).strftime('%H:%M'),
#                 'sunset': datetime.fromtimestamp(current['sys']['sunset']).strftime('%H:%M'),
#                 'timestamp': datetime.now().isoformat()
#             }
            
#         except Exception as e:
#             print(f"Error fetching weather: {e}")
#             return self._get_mock_weather()
    
#     def _fetch_met_eireann(self):
#         """Fetch from Met Éireann (stub for now)"""
#         # TODO: Implement Met Éireann API when available
#         return self._get_mock_weather()
    
#     def _get_mock_weather(self):
#         """Return mock weather data for testing"""
#         return {
#             'current_temp': 7,
#             'high': 11,
#             'low': 4,
#             'rain_chance': 20,
#             'description': 'partly cloudy',
#             'sunrise': '08:12',
#             'sunset': '17:34',
#             'timestamp': datetime.now().isoformat()
#         }
    
#     def _load_cache(self):
#         """Load weather data from cache if fresh"""
#         if not os.path.exists(self.cache_file):
#             return None
            
#         try:
#             with open(self.cache_file, 'r') as f:
#                 data = json.load(f)
                
#             # Check if cache is still fresh
#             cache_time = datetime.fromisoformat(data['timestamp'])
#             cache_duration = timedelta(seconds=self.config['weather']['cache_duration'])
            
#             if datetime.now() - cache_time < cache_duration:
#                 print("Using cached weather data")
#                 return data
                
#         except Exception as e:
#             print(f"Error loading cache: {e}")
            
#         return None
    
#     def _save_cache(self, data):
#         """Save weather data to cache"""
#         try:
#             os.makedirs(self.cache_dir, exist_ok=True)
#             with open(self.cache_file, 'w') as f:
#                 json.dump(data, f)
#         except Exception as e:
#             print(f"Error saving cache: {e}")


# def get_weather_data(config):
#     """Convenience function to get weather data"""
#     provider = WeatherProvider(config)
#     return provider.get_weather()