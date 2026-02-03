import requests
from app.data.generator import generate_events

BASE = "http://127.0.0.1:8000"

def main():
    # Create anomalous window
    events = generate_events(n=200, anomaly=True, seed=7)

    r = requests.post(f"{BASE}/analyze", json={"events": events, "top_k": 3}, timeout=60)
    r.raise_for_status()
    report = r.json()

    print("\n=== Diagnostic Report ===")
    print("Anomaly:", report["is_anomaly"])
    print("Score:", report["anomaly_score"])
    print("\nSuspected Root Causes:")
    for c in report["suspected_root_causes"]:
        print(" -", c)

    print("\nEvidence (Similar Incidents):")
    for e in report["evidence"]:
        print(f" - {e['title']} (sim={e['similarity']:.3f}) | {e['summary']}")

    print("\nRecommended Actions:")
    for a in report["recommended_actions"]:
        print(" -", a)

    print("\nExplanation:")
    print(report["explanation"])

if __name__ == "__main__":
    main()
