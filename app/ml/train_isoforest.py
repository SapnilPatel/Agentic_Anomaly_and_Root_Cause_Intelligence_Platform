import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

def train_isoforest(X: np.ndarray, model_dir: str, contamination: float = 0.03) -> str:
    os.makedirs(model_dir, exist_ok=True)
    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X)
    path = os.path.join(model_dir, "isoforest.joblib")
    joblib.dump(model, path)
    return path
