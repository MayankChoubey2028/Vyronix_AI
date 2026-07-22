from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embedding_model):

    db = FAISS.from_documents(
        chunks,
        embedding_model
    )

    db.save_local("vectorstore")

    return db


def load_vector_store(embedding_model):

    db = FAISS.load_local(
        "vectorstore",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db