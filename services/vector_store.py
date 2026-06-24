from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

CHROMA_PATH = "./chroma_db"


def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )


def get_vector_store():
    """
    Возвращает существующую ChromaDB или создает новую.
    """
    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="documents"
    )

    return vector_store