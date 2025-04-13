# interception.py (update for real-time support)

import random
import math
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import json
import warnings
from missile_generator import generate_missile_data
# ---------- Utility Functions ----------


def generate_missile_batch(n: int = 5):
    missile_batch = []
    missile_info_log = []

    for _ in range(n):
        data = generate_missile_data()
        missile_batch.append(data["Coordinates"])
        missile_info_log.append(data)  # Save full metadata if you want it later

    return missile_batch, missile_info_log

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def time_to_reach(point: Tuple[float, float], start: Tuple[float, float], speed: float) -> float:
    return distance(start, point) / speed

def estimate_risk(interception_point: Tuple[float, float]) -> float:
    lat, lon = interception_point
    altitude_risk = max(0, (18.5 - lat) * 1000)
    population_risk = max(0, (lon - 73.8) * 1000)
    return altitude_risk + population_risk

def calculate_heading(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1
    heading_rad = math.atan2(delta_lat, delta_lon)
    heading_deg = math.degrees(heading_rad)
    return (heading_deg + 360) % 360

def generate_missile_path(start_lat: float, start_lon: float, end_lat: float, end_lon: float, speed: float = 1.0, steps: int = 50) -> List[Tuple[float, float]]:
    lat_step = (end_lat - start_lat) / steps
    lon_step = (end_lon - start_lon) / steps
    return [(start_lat + i * lat_step, start_lon + i * lon_step) for i in range(steps + 1)]

def simulate_missile_trajectory(start_pos: Tuple[float, float], speed: float, heading_deg: float, steps: int = 50) -> List[Tuple[float, float]]:
    path = [start_pos]
    lat, lon = start_pos
    heading_rad = math.radians(heading_deg)
    for _ in range(steps):
        lat += math.sin(heading_rad) * speed
        lon += math.cos(heading_rad) * speed
        path.append((lat, lon))
    return path


# ---------- Core Simulation Functions ----------
def monte_carlo_interception_with_success(
    path: List[Tuple[float, float]],
    bases: List[Tuple[float, float]],
    missile_speeds: List[float],
    interceptor_speeds: List[float],
    samples: int = 50
) -> Tuple[List[dict], Optional[dict]]:
    all_results = []
    warning_note = None

    for _ in range(samples):
        point = random.choice(path)
        for base in bases:
            for m_speed in missile_speeds:
                for i_speed in interceptor_speeds:
                    missile_time = time_to_reach(point, path[0], m_speed)
                    interceptor_time = time_to_reach(point, base, i_speed)
                    success = interceptor_time <= missile_time
                    risk = estimate_risk(point)
                    result = {
                        "interception_point": point,
                        "base": base,
                        "missile_speed": m_speed,
                        "interceptor_speed": i_speed,
                        "missile_time": missile_time,
                        "interceptor_time": interceptor_time,
                        "success": success,
                        "risk_score": risk,
                        "success_probability": round(1 - (interceptor_time / missile_time), 3) if success else 0.0
                    }
                    all_results.append(result)

    successful_results = [r for r in all_results if r["success"]]
    top_5_results = sorted(successful_results, key=lambda r: r["risk_score"])[:5] if successful_results else []
    best_result = top_5_results[0] if top_5_results else None

    if not top_5_results:
        warning_msg = "No successful interception found in Monte Carlo simulation."
        warnings.warn(warning_msg)
        warning_note = {"warning": warning_msg}
        return [warning_note], None

    return top_5_results, best_result

def run_simulations(
    path: List[Tuple[float, float]],
    bases: List[Tuple[float, float]],
    missile_speeds: List[float],
    interceptor_speeds: List[float],
    samples: int = 50,
    sort_for_json: bool = True
) -> Tuple[List[dict], Optional[dict]]:
    results = []
    for m_speed in missile_speeds:
        for i_speed in interceptor_speeds:
            for base in bases:
                result = monte_carlo_interception_with_success(
                    path, base, i_speed, m_speed, samples
                )
                result.update({
                    "missile_speed": m_speed,
                    "interceptor_speed": i_speed
                })
                results.append(result)

    successful = [r for r in results if r['success']]
    successful.sort(key=lambda x: (x['risk_score'], -x['success_probability'], x['missile_time'], x['interceptor_time']))
    best_result = successful[0] if successful else None


    if sort_for_json:
        results.sort(key=lambda x: (
            x["risk_score"] if x["success"] else float('inf'),
            -x["success_probability"] if x["success"] else 0.0,
            x["missile_time"] if x["success"] else float('inf'),
            x["interceptor_time"] if x["success"] else float('inf')
        ))

    return results, best_result

def run_simulations_multiple(
    paths: List[List[Tuple[float, float]]],
    bases: List[Tuple[float, float]],
    missile_speeds: List[float],
    interceptor_speeds: List[float],
    samples: int = 50
) -> List[dict]:
    all_results = []
    for path in paths:
        results, best = run_simulations(path, bases, missile_speeds, interceptor_speeds, samples)
        if best:
            all_results.append(best)
    return all_results

def alert_if_unintercepted(missile_paths: List[List[Tuple[float, float]]], results: List[dict]):
    for i, (path, result) in enumerate(zip(missile_paths, results)):
        if not result['success']:
            last_point = path[-1]
            print(f"âš ï¸  ALERT: Missile {i+1} entered airspace and was NOT intercepted! Impact near {last_point}")


def plot_all_missiles(
    paths: List[List[Tuple[float, float]]],
    results: List[Optional[dict]],
    bases: List[Tuple[float, float]]
):
    base_names = [
        "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
        "Ahmedabad", "Jaipur", "Hyderabad", "Surat", "Lucknow", "Visakhapatnam"
    ]

    plt.figure(figsize=(12, 10))

    for (lat, lon), name in zip(bases, base_names):
        plt.scatter(lon, lat, color='blue', s=100)
        plt.text(lon + 0.1, lat, name, fontsize=9)

    for i, (path, result) in enumerate(zip(paths, results)):
        if not result:
            continue  # Skip if result is None

        lats, lons = zip(*path)
        plt.plot(lons, lats, linestyle='--', color='red', label='Missile Path' if i == 0 else "")

        point = result.get("missile_position") or result.get("interception_point")
        base = result.get("base", {}).get("coordinates") if isinstance(result.get("base"), dict) else result.get("base")

        if point and base:
            plt.plot([base[1], point[1]], [base[0], point[0]], color='green', linestyle=':', label='Interceptor Path' if i == 0 else "")
            plt.plot(point[1], point[0], 'go', markersize=8)

        final_lat, final_lon = path[-1]
        plt.plot(final_lon, final_lat, 'rx')
        plt.text(final_lon + 0.1, final_lat, f"Impact {i+1}", fontsize=8, color='red')

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Missile Interception Simulation")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("interception_map.png", dpi=300)
    plt.close()