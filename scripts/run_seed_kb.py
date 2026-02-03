from app.config import settings
from app.agents.retriever import build_embedder
from app.rag.vector_store import VectorStore
from app.rag.seed_kb import seed_incident_kb

def main():
    embedder = build_embedder(prefer_st=True)
    vs = VectorStore(settings.chroma_dir, settings.collection_name, embedder)
    docs = seed_incident_kb()
    vs.add_docs(docs)
    print(f"Seeded {len(docs)} incident docs into Chroma collection '{settings.collection_name}'")

if __name__ == "__main__":
    main()
