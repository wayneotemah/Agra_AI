from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import uuid

from django.conf import settings
from Engine.prompts import llm_answer, tts


# Create your views here.
# def index(request):
#     return HttpResponse('Hello, World!')

class TextQueryView(APIView):
    """
    View to handle text chat requests
    """
    def post(self, request):
        try:
            query = request.data.get("query")
            if query is None:
                return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
            response = llm_answer(query)
            context = {"response": response}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AudioQueryView(APIView):
    """
    View to handle text-to-speech requests
    """
    def post(self, request):
        try:
            # generate response using llm_answer
            query = request.data.get("query")
            if query is None:
                return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

            response = llm_answer(query)
            # convert response to speech

            filename = f"{uuid.uuid4()}.mp3"
            if tts(response,filename):
                audio_file_url = os.path.join(settings.STATIC_URL, "audio", filename)
                return Response({'query': query, 'audio_file_url': audio_file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Error in converting text to speech"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"error": "Could not process the request", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)