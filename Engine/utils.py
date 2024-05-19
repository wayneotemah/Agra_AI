from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()

class DocumentSearch:
    def __init__(self):
        # path to the directory wwith agra documents
        self.file_path = os.path.join(os.getcwd(), 'media',"my_docs")
        logger.info("Initializing database with documents from agra")

        
        # load documents from specified directory
        documents = self.load_data(self.file_path)

        # split documents into chunks for vectorization
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

        # initialize chroma vector store with specified collection name and persistent db
        self.vector_store = Chroma(
            collection_name="agra_docs",
            embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
            persist_directory=vdb_path
        )


    def load_data(self, file_path):
        """
        Load documents from specified directory
        """

        loader = DirectoryLoader(self.file_path, glob="*.pdf", loader_cls=PyPDFLoader)

        # ensure documents are loaded
        documents = loader.load()
        if not documents:
            raise ValueError("No documents were loaded. Ensure file path and file format is correct")

        return documents

    

    def search(self, query):
        """
        perform search on the vector store
        """
        embedding_vector = self.embedded_model.embed_query(query)
        docs = self.get_vector_store().similarity_search_by_vector(embedding_vector, k=5)
        return docs

# instantiate the document search
doc_search = DocumentSearch()

# make service available for import
__all__ = ["doc_search"]