import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict

SERVICES = ["api-gateway", "auth-service", "recommender-service", "billing-service"]

def generate_events(n: int = 200, anomaly: bool = False, seed: int = 42) -> List[Dict]:
    rng = np.random.default_rng(seed)
    start = datetime.utcnow() - timedelta(minutes=n)

    events = []
    for i in range(n):
        ts = (start + timedelta(minutes=i)).isoformat() + "Z"
        svc = rng.choice(SERVICES)

        # baseline
        latency = float(rng.normal(220, 40))
        err = float(max(0.0, rng.normal(0.02, 0.01)))
        cpu = float(np.clip(rng.normal(45, 15), 1, 95))
        msg = "ok"

        if anomaly and i > int(n * 0.75):
            # inject service-specific anomalies
            if svc == "api-gateway":
                latency = float(rng.normal(700, 120))
                err = float(max(0.0, rng.normal(0.08, 0.03)))
                msg = "dns resolve timeout upstream"
            elif svc == "auth-service":
                err = float(max(0.0, rng.normal(0.25, 0.05)))
                latency = float(rng.normal(420, 80))
                msg = "tls cert expired handshake failure"
            elif svc == "recommender-service":
                cpu = float(np.clip(rng.normal(92, 3), 1, 99))
                latency = float(rng.normal(520, 90))
                err = float(max(0.0, rng.normal(0.12, 0.04)))
                msg = "cpu saturation possible runaway batch job"
            else:
                latency = float(rng.normal(480, 60))
                err = float(max(0.0, rng.normal(0.10, 0.03)))
                msg = "kafka lag rebalance delays"

        events.append({
            "timestamp": ts,
            "service": svc,
            "latency_ms": float(max(1.0, latency)),
            "error_rate": float(min(1.0, max(0.0, err))),
            "cpu": float(min(100.0, max(0.0, cpu))),
            "message": msg,
        })
    return events
