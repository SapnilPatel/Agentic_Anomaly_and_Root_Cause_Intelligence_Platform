from typing import List, Dict, Any

class ExplanationAgent:
    def build_actions(self, suspected_causes: List[str], evidence_titles: List[str]) -> List[str]:
        actions = []
        text = " ".join(suspected_causes).lower() + " " + " ".join(evidence_titles).lower()

        if "tls" in text or "cert" in text:
            actions += ["Check certificate expiry and renewal automation", "Validate TLS handshake errors in logs"]
        if "dns" in text:
            actions += ["Check recent config/rollout related to DNS/resolvers", "Validate upstream resolution latency and timeouts"]
        if "cpu" in text or "runaway" in text:
            actions += ["Inspect batch jobs / cron triggers", "Apply rate limits or autoscale CPU-bound service"]
        if "kafka" in text or "lag" in text:
            actions += ["Check consumer lag metrics and partition balance", "Inspect recent deploys affecting consumer throughput"]

        if not actions:
            actions = ["Check recent deployments and config changes", "Compare traffic patterns vs baseline", "Inspect dependency health dashboards"]

        # keep unique
        seen = set()
        out = []
        for a in actions:
            if a not in seen:
                out.append(a); seen.add(a)
        return out

    def summarize(self, is_anomaly: bool, anomaly_score: float, suspected: List[str], evidence: List[Dict[str, Any]]) -> str:
        ev_titles = [e["title"] for e in evidence]
        if is_anomaly:
            return (
                f"Detected an anomalous pattern (score={anomaly_score:.3f}). "
                f"Top suspected root causes: {', '.join(suspected[:2])}. "
                f"Similar past incidents: {', '.join(ev_titles) if ev_titles else 'none found'}."
            )
        return f"No anomaly detected (score={anomaly_score:.3f}). System behavior appears within baseline."
