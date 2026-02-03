import os
import joblib
import numpy as np
from typing import Tuple
from app.ml.model import to_features
from app.config import settings

class AnomalyDetectorAgent:
    def __init__(self):
        self.model_path = os.path.join(settings.model_dir, "isoforest.joblib")
        if not os.path.exists(self.model_path):
            raise RuntimeError(f"Model not found at {self.model_path}. Train it first (scripts/run_train.py).")
        self.model = joblib.load(self.model_path)

    def detect(self, events) -> Tuple[bool, float, dict]:
        fv = to_features(events)
        # IsolationForest: higher is more normal via score_samples; invert for anomaly_score
        normal_score = self.model.score_samples(fv.X).mean()
        anomaly_score = float(-normal_score)  # higher => more anomalous
        # You can tune threshold; keep simple
        is_anomaly = anomaly_score > 0.55
        debug = {"mean_normal_score": float(normal_score), "feature_means": fv.X.mean(axis=0).tolist()}
        return is_anomaly, anomaly_score, debug
