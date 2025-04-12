# missile_simulator.py

import time
import requests
import random
import math
from datetime import datetime


BACKEND_URL = "http://127.0.0.1:8080/api/missile-data"  

def random_position():
    lat = random.uniform(10.0, 20.0)  
    lon = random.uniform(70.0, 90.0)  
    return lat, lon

def move_position(lat, lon, speed_mps, direction_deg):
    distance_deg = (speed_mps / 1000.0) / 111  
    rad = math.radians(direction_deg)
    new_lat = lat + distance_deg * math.cos(rad)
    new_lon = lon + distance_deg * math.sin(rad)
    return new_lat, new_lon

# Simulate one missile
def simulate_missile(missile_id):
    lat, lon = random_position()
    speed_mps = random.uniform(1000, 3000)  # Speed between 1000 and 3000 meters per second
    direction_deg = random.uniform(0, 360)  # Any random direction
    altitude_m = random.uniform(5000, 15000)  # Altitude between 5km and 15km

    for i in range(30):  # Simulate 30 seconds of flight
        missile_data = {
            "missileId": missile_id,
            "launchTime": datetime.utcnow().isoformat() + "Z",
            "currentPosition": {
                "latitude": lat,
                "longitude": lon
            },
            "speed_mps": speed_mps,
            "direction_deg": direction_deg,
            "altitude_m": altitude_m
        }

        try:
            response = requests.post(BACKEND_URL, json=missile_data)
            print(f"Sent missile update: {missile_data} Status: {response.status_code}")
        except Exception as e:
            print(f"Error sending data: {e}")

        # Move missile for next second
        lat, lon = move_position(lat, lon, speed_mps, direction_deg)
        time.sleep(1)  # Wait for 1 second

# Main simulation loop
if __name__ == "__main__":
    print("Starting Missile Simulator...")
    missile_count = 1
    while True:
        missile_id = f"MIDAS-{missile_count}"
        simulate_missile(missile_id)
        missile_count += 1
        time.sleep(random.randint(10, 20))  # Launch a new missile every 10-20 seconds
