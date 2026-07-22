from langchain_community.document_loaders import TextLoader


def load_text(path: str):

    loader = TextLoader(path)

    documents = loader.load()

    return documents