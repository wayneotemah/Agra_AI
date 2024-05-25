from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Engine.prompts import llm_answer, tts

import os
from django.conf import settings


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

            # convert response to speech
            audio_file_path = tts(query)
            print(audio_file_path)
            if audio_file_path:
                audio_file_url = os.path.join(settings.STATIC_URL, "audio", os.path.basename(audio_file_path))
                print(audio_file_url)
                print(query)
                return Response({'query': query, 'audio_file_url': audio_file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Error in converting text to speech"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"error": "Could not process the request", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)