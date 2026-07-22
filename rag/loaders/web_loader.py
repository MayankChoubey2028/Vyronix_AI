from langchain_community.document_loaders import WebBaseLoader


def load_web(url: str):

    loader = WebBaseLoader(url)

    documents = loader.load()

    return documents