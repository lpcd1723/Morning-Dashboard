import os
import time
import json

def get_cached_data(cache_file, max_age_seconds):
    if os.path.exists(cache_file):
        file_age = time.time() - os.path.gettime(cache_file)
        if file_age < max_age_seconds:
            with open(cache_file, "r") as f:
                return json.load(f)
        return None
def save_to_cache(cache_file, data):
    with open(cache_file, "w") as f:
        json.dump(data, f)