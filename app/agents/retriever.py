from typing import List

class SimpleEmbedder:
    """Fallback embedder: cheap hashing-based embeddings (works offline, no downloads)."""
    def __init__(self, dim: int = 256):
        self.dim = dim

    def _hash(self, s: str) -> int:
        h = 2166136261
        for c in s:
            h ^= ord(c)
            h *= 16777619
            h &= 0xFFFFFFFF
        return h

    def embed(self, texts: List[str]):
        import numpy as np
        out = []
        for t in texts:
            v = np.zeros(self.dim, dtype="float32")
            for tok in t.lower().split():
                idx = self._hash(tok) % self.dim
                v[idx] += 1.0
            # normalize
            n = float((v**2).sum() ** 0.5) + 1e-9
            out.append((v / n).tolist())
        return out

class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]):
        embs = self.model.encode(texts, normalize_embeddings=True)
        return embs.tolist()

def build_embedder(prefer_st: bool = True):
    if not prefer_st:
        return SimpleEmbedder()
    try:
        return SentenceTransformerEmbedder()
    except Exception:
        # If model download fails, fallback silently
        return SimpleEmbedder()
