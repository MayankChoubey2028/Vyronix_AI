def retrieve(query, db, k=4):

    results = db.similarity_search(
        query,
        k=k
    )

    return results