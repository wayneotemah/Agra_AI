from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_openai import OpenAIEmbeddings

from django.conf import settings

from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

# path to the directory where the vector store will be persisted
vdb_path = os.path.join(os.getcwd(), "vdb")

class DocumentSearch:
    def __init__(self):
        # path to the directory wwith agra documents
        self.file_path = os.path.join(os.getcwd(), 'media',"my_docs")
        logger.info("Initializing database with documents from agra")

        try:        
            # load documents from specified directory
            documents = self.load_data(self.file_path)

            # split documents into chunks for vectorization
            child_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

            # initialize chroma vector store with specified collection name and persistent db
            self.vectorstore = Chroma(
                collection_name="agra_docs",
                embedding_function = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
            )

            # storage layer for the parent documents
            store = InMemoryStore()

            self.retriever = ParentDocumentRetriever(
                vectorstore=self.vectorstore,
                docstore=store,
                child_splitter=child_splitter,
                parent_splitter=None,
            )

            self.retriever.add_documents(documents)

        except Exception as e:
            logger.error(f"Error occured when initializing the database: {e}")
            raise e

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
        if query is None:
            raise ValueError("Query cannot be None")
        # result = self.vectorstore.similarity_search(query)
        result = self.retriever.invoke(query)
        return result

# instantiate the document search
doc_search = DocumentSearch()

# make service available for import
__all__ = ["doc_search"]