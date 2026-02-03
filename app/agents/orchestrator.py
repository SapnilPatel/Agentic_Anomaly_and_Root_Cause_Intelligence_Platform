from typing import List, Dict, Any
from app.agents.detector import AnomalyDetectorAgent
from app.agents.rca import RootCauseAgent
from app.agents.retriever import build_embedder
from app.rag.vector_store import VectorStore
from app.config import settings
from app.agents.explainer import ExplanationAgent

class Orchestrator:
    def __init__(self):
        self.detector = AnomalyDetectorAgent()
        self.rca = RootCauseAgent()
        self.explainer = ExplanationAgent()

        embedder = build_embedder(prefer_st=True)
        self.vs = VectorStore(
            persist_dir=settings.chroma_dir,
            collection_name=settings.collection_name,
            embedder=embedder
        )

    def analyze(self, events, top_k: int = 3) -> Dict[str, Any]:
        is_anomaly, anomaly_score, debug = self.detector.detect(events)

        suspected = []
        evidence = []

        if is_anomaly:
            suspected = self.rca.infer(events)

            # Build query from summary of event messages + services
            svc_list = sorted(list({e.service for e in events}))
            msg_blob = " ".join([e.message for e in events if e.message]).strip()
            query = f"services={','.join(svc_list)} symptoms={msg_blob} latency/error/cpu anomaly"

            hits = self.vs.query(query, top_k=top_k)
            for sim, doc, md in hits:
                evidence.append({
                    "title": md.get("title", "incident"),
                    "similarity": float(sim),
                    "summary": md.get("summary", doc[:160]),
                    "tags": md.get("tags", []),
                })

        actions = self.explainer.build_actions(suspected, [e["title"] for e in evidence]) if is_anomaly else []
        explanation = self.explainer.summarize(is_anomaly, anomaly_score, suspected, evidence)

        return {
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": float(anomaly_score),
            "suspected_root_causes": suspected,
            "evidence": evidence,
            "recommended_actions": actions,
            "explanation": explanation,
            "debug": debug,
        }
