from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from .utils import doc_search

from transformers import AutoTokenizer, AutoModelForTextToWaveform

import uuid
import torch
import torchaudio
from django.conf import settings
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

torchaudio.set_audio_backend("sox_io")

model = ChatGroq(model_name="llama3-70b-8192", api_key=os.getenv("groq_api_key"))

system = "You are Agra AI Assistant, a helpful chatbot that can answer questions about The AGRA (Allinace for Green Revolution in Africa) using using the provided context"



tts_tokenizer = AutoTokenizer.from_pretrained("./Engine/models/vits-ljs")
tts_model = AutoModelForTextToWaveform.from_pretrained("./Engine/models/vits-ljs")


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

def tts(text, filename=None):
    """
    Convert text to speech
    """
    try:
        # load tokenizer and model
        tokenizer = tts_tokenizer
        model = tts_model

        # tokenize the input text
        inputs = tokenizer(text, return_tensors="pt")

        # generate speech from the model
        with torch.no_grad():
            waveform = model(inputs["input_ids"])

        # define a static path to save the audio file
        static_audio_dir = os.path.join(settings.BASE_DIR, "static", "audio")

        # create a dir if it does not exist
        os.makedirs(static_audio_dir, exist_ok=True)

        # set the filename for the audio
        if not filename:
            filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(static_audio_dir, filename)

        # Save the audio file using torchaudio
        waveform_tensor = torch.from_numpy(waveform[0].squeeze().cpu().numpy().astype("float32")).unsqueeze(0)
        filepath = os.path.join(static_audio_dir, filename)
        torchaudio.save(filepath, waveform_tensor, sample_rate=22050, format='mp3')

        return True

    except Exception as e:
        logger.error(f"Error in converting text to speech: {e}")
        return None



