from rag.loaders.universal_loader import load

from rag.text_splitter import split_documents

from rag.embedder import get_embedding_model

from rag.vector_store import (
    create_vector_store,
    load_vector_store
)

from rag.retriever import retrieve


def ingest(source: str):
    """
    Build or rebuild the vector database from a source.
    Returns the db object so the caller can keep it in memory
    (avoids reloading from disk on every query).
    """

    documents = load(source)

    chunks = split_documents(documents)

    embedding_model = get_embedding_model()

    db = create_vector_store(
        chunks,
        embedding_model
    )

    return db


def query(question: str):
    """
    Standalone query that loads the db from disk each time.
    Useful for quick scripts/tests, but NOT used by the live backend
    (the backend keeps db in memory - see search_rag below).
    """

    embedding_model = get_embedding_model()

    db = load_vector_store(
        embedding_model
    )

    results = retrieve(
        question,
        db
    )

    return results


def search_rag(question: str, db):
    """
    Query against an already-loaded db object (kept in memory by the backend).
    This is what agent/tools.py should call.
    """

    return retrieve(question, db)