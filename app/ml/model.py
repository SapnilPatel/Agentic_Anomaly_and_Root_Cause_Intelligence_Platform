from dataclasses import dataclass
from typing import List, Dict
import numpy as np

FEATURES = ["latency_ms", "error_rate", "cpu"]

@dataclass
class FeatureVector:
    X: np.ndarray
    meta: List[Dict]

def to_features(events) -> FeatureVector:
    X = []
    meta = []
    for e in events:
        X.append([float(e.latency_ms), float(e.error_rate), float(e.cpu)])
        meta.append({"timestamp": e.timestamp, "service": e.service, "message": e.message})
    return FeatureVector(X=np.array(X, dtype=np.float32), meta=meta)
