from typing import List, Dict

class RootCauseAgent:
    """
    Lightweight RCA heuristics (good for a demo).
    In interviews, you can describe how to replace this with causal models, SHAP, etc.
    """
    def infer(self, events) -> List[str]:
        # Aggregate by service
        services = {}
        for e in events:
            s = e.service
            services.setdefault(s, {"lat": [], "err": [], "cpu": [], "msg": []})
            services[s]["lat"].append(float(e.latency_ms))
            services[s]["err"].append(float(e.error_rate))
            services[s]["cpu"].append(float(e.cpu))
            if e.message:
                services[s]["msg"].append(e.message.lower())

        causes = []

        # Simple heuristics
        for svc, v in services.items():
            lat = sum(v["lat"]) / max(len(v["lat"]), 1)
            err = sum(v["err"]) / max(len(v["err"]), 1)
            cpu = sum(v["cpu"]) / max(len(v["cpu"]), 1)
            msgs = " ".join(v["msg"])

            if err > 0.12 and ("tls" in msgs or "cert" in msgs):
                causes.append(f"{svc}: possible certificate/TLS issue (errors high + cert keywords)")
            if lat > 450 and ("dns" in msgs or "resolve" in msgs):
                causes.append(f"{svc}: possible DNS/resolution issue (latency high + dns keywords)")
            if cpu > 85 and (lat > 350 or err > 0.08):
                causes.append(f"{svc}: CPU saturation or runaway workload (cpu high + latency/errors)")
            if "kafka" in msgs and ("lag" in msgs or "rebalance" in msgs):
                causes.append(f"{svc}: kafka consumer lag / rebalancing (kafka keywords)")

        if not causes:
            causes.append("No obvious signature — likely multi-factor (config drift, dependency regression, or traffic spike).")

        return causes
