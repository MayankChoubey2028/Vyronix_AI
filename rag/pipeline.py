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

    embedding_model = get_embedding_model()

    db = load_vector_store(
        embedding_model
    )

    results = retrieve(
        question,
        db
    )

    return results