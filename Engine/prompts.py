from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from .utils import doc_search

from django.conf import settings
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)


model = ChatGroq(model_name="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY"))

system = "Agra AI Assistant"


def llm_query(user_input: str, context: str) -> str:
    """
    Perform search on the vector store
    """
    try:
        human_message = f"user input: {user_input}\ndocument context: {context}"

        # chat template with the system and human messages
        chat_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(system)),
                HumanMessagePromptTemplate.from_template(human_message),
            ])

        # format the messages with the context and user input
        messages = chat_template.format_messages(
            context=context,
            user_input=user_input
        )

        # get the response from the model
        data = model.invoke(messages)
        for item in data:
            if item[0] == "content":
                response = item[1]
                break
        return response

    except Exception as e:
        logger.error(f"Error in formatting messages: {e}")
        return "An error occurred. Please try again."

        
def llm_answer(user_input: str) -> str:
    context_results = doc_search.search(user_input)
    context = context_results[0].page_content if context_results else "No context found"

    # get the response from the model using the retrieved documents
    return llm_query(user_input=user_input, context=context)

  