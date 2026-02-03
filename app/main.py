from fastapi import FastAPI
from app.schemas import IngestRequest, AnalyzeRequest, DiagnosticReport
from app.agents.orchestrator import Orchestrator

app = FastAPI(title="Agentic Anomaly & RCA Platform", version="1.0.0")

# In-memory store (for demo); in enterprise you’d persist to Kafka/S3/DB
EVENT_BUFFER = []

orch = None

@app.on_event("startup")
def _startup():
    global orch
    orch = Orchestrator()

@app.post("/ingest")
def ingest(req: IngestRequest):
    EVENT_BUFFER.extend(req.events)
    return {"status": "ok", "buffer_size": len(EVENT_BUFFER)}

@app.post("/analyze", response_model=DiagnosticReport)
def analyze(req: AnalyzeRequest):
    result = orch.analyze(req.events, top_k=req.top_k)
    return result
