from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings 
from backend.config.settings import DATA_DIR

def load():
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob = "**/*.pdf",
        loader_cls = PyPDFLoader
    )
    documents = loader.load()
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def load_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings
