from typing import List, Dict, Any

def seed_incident_kb() -> List[Dict[str, Any]]:
    # Small but realistic incident KB (you can expand later)
    kb = [
        {
            "id": "inc_001",
            "text": "Latency spikes in api-gateway caused by downstream DNS resolution failures after config update. Errors increased, CPU normal.",
            "metadata": {"title": "DNS failure after config change", "tags": ["latency", "api-gateway", "dns", "config-drift"], "summary": "DNS resolution failures after a rollout caused latency spikes."}
        },
        {
            "id": "inc_002",
            "text": "High error rate in auth-service due to expired TLS certificate. Latency moderate, CPU low. Root cause was missing renewal automation.",
            "metadata": {"title": "Expired TLS certificate", "tags": ["errors", "auth-service", "tls", "ops"], "summary": "Certificate expiration caused authentication failures."}
        },
        {
            "id": "inc_003",
            "text": "CPU saturation in recommender-service due to runaway batch job. Latency increased and error rate rose from timeouts.",
            "metadata": {"title": "Runaway batch job CPU saturation", "tags": ["cpu", "timeouts", "batch-job"], "summary": "Unexpected batch workload saturated CPU leading to timeouts."}
        },
        {
            "id": "inc_004",
            "text": "Kafka consumer lag increased leading to delayed processing. Symptoms included rising latency and intermittent errors across dependent services.",
            "metadata": {"title": "Kafka consumer lag", "tags": ["kafka", "lag", "pipeline"], "summary": "Consumer lag led to cascading delays and intermittent failures."}
        },
        {
            "id": "inc_005",
            "text": "Vector database index rebuild caused query latency regression. CPU increased slightly; error rate stayed low.",
            "metadata": {"title": "Vector index rebuild latency regression", "tags": ["vector-db", "search", "latency"], "summary": "Index maintenance led to search latency regression."}
        },
    ]
    return kb
