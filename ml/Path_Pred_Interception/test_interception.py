# test_interception_sim.py

import json
from datetime import datetime, timezone
from interception import (
    time_to_reach,
    calculate_heading,
    monte_carlo_interception_with_success,
    plot_all_missiles,
    estimate_risk,
    distance,
    generate_missile_batch
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
    (17.68, 83.22)    # Visakhapatnam
]

# Base names for reporting
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

# Simulated real-time missile positions
real_time_missile_paths, missile_info_log = generate_missile_batch()

missile_speed = 2.0
interceptor_speed = 3.0
samples = 50

enriched_results = []

for missile_id, path in enumerate(real_time_missile_paths, 1):
    all_results, best_result = monte_carlo_interception_with_success(
        path, interceptor_bases, [missile_speed], [interceptor_speed], samples=samples
    )

    if all_results and 'warning' in all_results[0]:
        enriched_results.append({
            "missile_id": missile_id,
            "monte_carlo_attempts": [],
            "monte_carlo_best": None,
            "warning": all_results[0]['warning']
        })
        continue

    for r in all_results:
        coords = tuple(r["base"]) if isinstance(r["base"], (list, tuple)) else tuple(r["base"]["coordinates"])
        r["base"] = {
            "name": base_names.get(coords, "Unknown"),
            "coordinates": list(coords)
        }
        r["distance"] = distance(r["base"]["coordinates"], r["interception_point"])
        r["method"] = "monte_carlo"

    if best_result:
        coords = tuple(best_result["base"]) if isinstance(best_result["base"], (list, tuple)) else tuple(best_result["base"]["coordinates"])
        best_result["base"] = {
            "name": base_names.get(coords, "Unknown"),
            "coordinates": list(coords)
        }
        best_result["distance"] = distance(best_result["base"]["coordinates"], best_result["interception_point"])
        best_result["method"] = "monte_carlo"

    enriched_entry = {
        "missile_id": missile_id,
        "interception_result": best_result
    }

    if all_results and 'warning' in all_results[0]:
        enriched_entry["warning"] = all_results[0]['warning']

    enriched_results.append(enriched_entry)


with open("monte_carlo_real_time_results.json", "w") as f:
    json.dump(enriched_results, f, indent=4)

plot_all_missiles(
    real_time_missile_paths,
    [entry["interception_result"] for entry in enriched_results],
    interceptor_bases
)
