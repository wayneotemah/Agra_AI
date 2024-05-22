import os
import django
from dotenv import load_dotenv
from Engine.utils import DocumentSearch
from Engine.prompts import llm_query, llm_answer

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MainApp.settings')
django.setup()

load_dotenv()

# Function to test DocumentSearch and print the output
def test_document_search():
    try:
        doc_search = DocumentSearch()
        query = 'Who is the president of AGRA?'
        results = doc_search.search(query)
        
        if not results:
            print("No documents found for the query.")
            return None
        
        #using the first result as the context
        context = results[0].page_content
        print("DocumentSearch results:")
        print(context)
        
        return context
    except Exception as e:
        print(f"Error testing DocumentSearch: {e}")
        return None

# Function to test llm_query and print the output
def test_llm_query(user_input, context):
    try:
        response = llm_query(user_input, context)
        print("llm_query response:")
        print(response)
    except Exception as e:
        print(f"Error testing llm_query: {e}")

# Function to test llm_answer and print the output
def test_llm_answer(user_input):
    try:
        response = llm_answer(user_input)
        print("llm_answer response:")
        print(response)
    except Exception as e:
        print(f"Error testing llm_answer: {e}")

if __name__ == "__main__":
    print("Testing DocumentSearch...")
    context = test_document_search()
    
    if context:
        print("\nTesting llm_query with document context...")
        test_llm_query('Who is the president of AGRA?', context)
        
        print("\nTesting llm_answer with document context...")
        test_llm_answer('Who is the president of AGRA?')
