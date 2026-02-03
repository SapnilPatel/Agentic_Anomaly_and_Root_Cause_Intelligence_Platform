from typing import List, Dict, Any, Tuple
import os
import chromadb
from chromadb.config import Settings as ChromaSettings

class VectorStore:
    def __init__(self, persist_dir: str, collection_name: str, embedder):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = embedder

    def add_docs(self, docs: List[Dict[str, Any]]) -> None:
        ids = [d["id"] for d in docs]
        texts = [d["text"] for d in docs]
        metadatas = [d.get("metadata", {}) for d in docs]
        embeddings = self.embedder.embed(texts)
        self.collection.upsert(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[float, str, Dict[str, Any]]]:
        emb = self.embedder.embed([text])[0]
        res = self.collection.query(query_embeddings=[emb], n_results=top_k, include=["documents", "metadatas", "distances"])
        out = []
        for doc, md, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            # Chroma returns distance; convert to similarity-ish score (lower dist => higher sim)
            sim = 1.0 / (1.0 + float(dist))
            out.append((sim, doc, md))
        return out
