from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Event(BaseModel):
    timestamp: str
    service: str
    latency_ms: float
    error_rate: float
    cpu: float
    message: str = ""

class IngestRequest(BaseModel):
    events: List[Event]

class AnalyzeRequest(BaseModel):
    events: List[Event]
    top_k: int = 3

class Evidence(BaseModel):
    title: str
    similarity: float
    summary: str
    tags: List[str] = []

class DiagnosticReport(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    suspected_root_causes: List[str]
    evidence: List[Evidence]
    recommended_actions: List[str]
    explanation: str
    debug: Optional[Dict[str, Any]] = None
