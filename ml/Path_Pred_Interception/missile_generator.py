import numpy as np
import random
from geopy.distance import geodesic

# Define launch regions (outside India)
launch_regions = [
    {"name": "West", "lat_range": (27.0, 32.0), "lon_range": (60.0, 68.0)},
    {"name": "North", "lat_range": (30.0, 36.0), "lon_range": (75.0, 85.0)},
    {"name": "East", "lat_range": (21.0, 27.0), "lon_range": (90.0, 95.0)},
    {"name": "South", "lat_range": (5.0, 10.0), "lon_range": (75.0, 80.0)}
]

# Define target region (India)
india_lat_range = (20.0, 28.0)
india_lon_range = (72.0, 88.0)

def generate_missile_data(steps=30, alt_start=80, alt_end=0, noise=0.002, interceptor_speed_kmps=3.0, time_per_step_sec=1.0):
    region = random.choice(launch_regions)
    start_lat = random.uniform(*region["lat_range"])
    start_lon = random.uniform(*region["lon_range"])
    target_lat = random.uniform(*india_lat_range)
    target_lon = random.uniform(*india_lon_range)

    latitudes = np.linspace(start_lat, target_lat, steps)
    longitudes = np.linspace(start_lon, target_lon, steps)
    altitudes = np.linspace(alt_start, alt_end, steps)

    latitudes += np.random.normal(0, noise, steps)
    longitudes += np.random.normal(0, noise, steps)

    total_distance_km = 0
    for i in range(steps - 1):
        p1 = (latitudes[i], longitudes[i])
        p2 = (latitudes[i + 1], longitudes[i + 1])
        total_distance_km += geodesic(p1, p2).km

    total_time_sec = (steps - 1) * time_per_step_sec
    average_missile_speed_kmps = round(total_distance_km / total_time_sec, 4)

    coordinates = [(round(float(lat), 3), round(float(lon), 3)) for lat, lon in zip(latitudes, longitudes)]

    return {
        "Coordinates": coordinates,
        "Altitudes_km": [round(float(a), 2) for a in altitudes],
        "Average_Missile_Speed_kmps": average_missile_speed_kmps,
        "Interceptor_Speed_kmps": interceptor_speed_kmps,
        "Time_Per_Step_sec": time_per_step_sec,
        "Total_Flight_Time_sec": total_time_sec,
        "Start_Coordinates": (round(start_lat, 3), round(start_lon, 3)),
        "Target_Coordinates": (round(target_lat, 3), round(target_lon, 3))
    }

# Generate and print missile data
missile_data = generate_missile_data()
