import numpy as np
from app.config import settings
from app.data.generator import generate_events
from app.ml.model import to_features
from app.ml.train_isoforest import train_isoforest

def main():
    # Train only on "normal" baseline
    events = generate_events(n=1200, anomaly=False, seed=1)
    from app.schemas import Event
    parsed = [Event(**e) for e in events]
    fv = to_features(parsed)
    path = train_isoforest(fv.X, settings.model_dir, contamination=0.03)
    print(f"Trained IsolationForest model saved at: {path}")

if __name__ == "__main__":
    main()
