import time
import random


def get_satellite_risk_score(location_name="Hsinchu Science Park, Taiwan (TSMC)", baseline=950.0):
    """
    Evaluates nightlight intensity drop and returns a normalized Satellite Risk Signal (0.0 to 1.0).
    THIS IS WHAT PHASE 5 CONSUMES.
    """
    # Simulate current reading
    current_brightness = baseline * random.uniform(0.75, 1.02)
    drop_percentage = ((baseline - current_brightness) / baseline) * 100.0

    if drop_percentage >= 20.0:
        # Severe blackout / production drop
        return min(round(drop_percentage / 50.0, 2), 1.0)
    elif drop_percentage > 5.0:
        # Minor anomaly
        return 0.30
    else:
        # Operational stability
        return 0.05


def check_nightlight_anomaly(location_name, baseline_brightness):
    """
    Keeps your terminal UI for testing Phase 4 visually!
    """
    print(f"🛰️ Pointing satellite sensors at: {location_name}...")
    time.sleep(1.5)  # Syncing with orbital data

    # Simulate current brightness readings for visual testing
    if random.random() > 0.75:
        current_brightness = baseline_brightness * random.uniform(0.60, 0.75)
    else:
        current_brightness = baseline_brightness * random.uniform(0.85, 1.05)

    drop_percentage = ((baseline_brightness - current_brightness) / baseline_brightness) * 100

    if drop_percentage >= 20.0:
        print(f"   ⚠️ ANOMALY DETECTED: {drop_percentage:.1f}% drop in nightlight intensity!")
    elif drop_percentage < 0:
        print(f"   ✅ Normal operations. Brightness increased by {abs(drop_percentage):.1f}%.")
    else:
        print(f"   ✅ Normal operations. Minor fluctuation of {drop_percentage:.1f}%.")

    # Show the Phase 5 normalized score calculation in the terminal
    normalized_score = get_satellite_risk_score(location_name, baseline_brightness)
    print(f"   🧬 NORMALIZED PHASE 5 SCORE: {normalized_score} / 1.0")


if __name__ == "__main__":
    print("🌍 INITIATING GEOSPATIAL TRUTH CHECK")
    print("=" * 65)

    # Key locations to monitor (Baseline measured in nanoWatts/cm2/sr)
    locations = {
        "Hsinchu Science Park, Taiwan (TSMC)": 950.0,
        "Port of Kaohsiung, Taiwan": 820.0,
        "ASML Veldhoven Facility, Netherlands": 610.0
    }

    for loc, baseline in locations.items():
        check_nightlight_anomaly(loc, baseline)
        print("-" * 65)