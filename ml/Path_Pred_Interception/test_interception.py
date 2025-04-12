# test_interception_sim.py
from interception import generate_missile_path
import json
# Define interceptor bases
bases = [
    (28.61, 77.21), (19.07, 72.87), (13.08, 80.27), (22.57, 88.36),
    (12.97, 77.59), (23.03, 72.58), (26.92, 75.80), (17.38, 78.48),
    (21.17, 72.83), (26.85, 80.95), (17.68, 83.22)
]

# Define missile paths
missiles = [
    generate_missile_path(33.0, 60.0, 25.0, 75.0),
    generate_missile_path(18.0, 60.0, 10.5, 75.0),
    generate_missile_path(30.0, 100.0, 20.0, 95.0)
]


from interception import (
    generate_missile_path,
    run_simulations_multiple,
    plot_all_missiles
)

# Define interceptor bases (lat, lon)
interceptor_bases = [
    (28.61, 77.21),   # Delhi
    (19.07, 72.87),   # Mumbai
    (13.08, 80.27),   # Chennai
    (22.57, 88.36),   # Kolkata
    (12.97, 77.59),   # Bengaluru
    (23.03, 72.58),   # Ahmedabad
    (26.92, 75.80),   # Jaipur
    (17.38, 78.48),   # Hyderabad
    (21.17, 72.83),   # Surat
    (26.85, 80.95),   # Lucknow
    (17.68, 83.22),   # Visakhapatnam
]

# Simulated missile paths
missile_paths = [
    generate_missile_path(33.0, 60.0, 25.0, 75.0),   # NW to West India
    generate_missile_path(18.0, 60.0, 10.5, 75.0),   # SW to South India
    generate_missile_path(30.0, 100.0, 20.0, 95.0),  # NE to East India
]

missile_speeds = [2.0]  # units per tick
interceptor_speeds = [3.0]  # faster than missiles

from datetime import datetime

base_names = {
    (28.61, 77.21): "Delhi",
    (19.07, 72.87): "Mumbai",
    (13.08, 80.27): "Chennai",
    (22.57, 88.36): "Kolkata",
    (12.97, 77.59): "Bengaluru",
    (23.03, 72.58): "Ahmedabad",
    (26.92, 75.80): "Jaipur",
    (17.38, 78.48): "Hyderabad",
    (21.17, 72.83): "Surat",
    (26.85, 80.95): "Lucknow",
    (17.68, 83.22): "Visakhapatnam"
}

# Run the simulation
raw_results = run_simulations_multiple(
    missile_paths, interceptor_bases, missile_speeds, interceptor_speeds, samples=50
)

# Enrich results with metadata
timestamp = datetime.utcnow().isoformat() + "Z"

enriched_results = []
for i, result in enumerate(raw_results):
    missile_path = missile_paths[i]
    enriched_results.append({
        "missile_id": i + 1,
        "missile_path": {
            "start": missile_path[0],
            "end": missile_path[-1],
            "waypoints": missile_path
        },
        "simulation_parameters": {
            "missile_speed": result["missile_speed"],
            "interceptor_speed": result["interceptor_speed"],
            "samples": 50
        },
        "base": {
            "name": base_names.get(tuple(result["base"]), "Unknown"),
            "coordinates": result["base"]
        },
        "interception_result": {
            "success": result["success"],
            "interception_point": result["interception_point"],
            "missile_time": result["missile_time"],
            "interceptor_time": result["interceptor_time"],
            "success_probability": result["success_probability"],
            "risk_score": result["risk_score"]
        },
        "alert": (
            f"Missile was NOT intercepted. Impact near {missile_path[-1]}"
            if not result["success"] else None
        ),
        "timestamp": timestamp,
        "rank": i + 1  # Optional: use your own logic for ranking
    })

with open("interception_results_detailed.json", "w") as f:
    json.dump(enriched_results, f, indent=4)

# Visualize the result
plot_all_missiles(missile_paths, raw_results, interceptor_bases)
