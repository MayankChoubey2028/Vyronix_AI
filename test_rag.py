"""
Standalone test for the RAG pipeline: web_loader -> splitter -> embedder -> vector store -> retriever

Run from your project ROOT (Vyronix_AI/) with:
    python test_rag.py

This file must sit in the project ROOT, next to your rag/ folder,
because it imports rag.pipeline as a package (from rag.pipeline import ...).
"""

import time

from rag.pipeline import ingest, query


URL = "https://midc-lab.github.io/home/index.html"


def main():
    print("=== RAG Pipeline Test (Web URL) ===\n")

    # 1. Ingest the URL (load -> split -> embed -> store)
    print(f"[1/2] Ingesting URL: {URL}")
    t0 = time.time()
    db = ingest(URL)
    t1 = time.time()
    print(f"OK - vector store built (took {t1 - t0:.2f}s)\n")

    # 2. Query with questions based on the page's actual content
    test_questions = [
        "What are the core research areas of this lab?",
        "How can a B.Tech student join the lab?",
        "What is the lab's email address?",
        "What is this lab affiliated with?",
    ]

    print("[2/2] Running test queries...\n")
    for q in test_questions:
        t0 = time.time()
        results = query(q)
        t1 = time.time()

        print(f"Query: {q}  (took {t1 - t0:.2f}s)")
        for i, r in enumerate(results, 1):
            print(f"  [{i}] {r.page_content[:200]}")
        print()

    print("=== RAG pipeline test complete ===")


if __name__ == "__main__":
    main()