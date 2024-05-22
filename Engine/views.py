from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Engine.prompts import llm_answer 

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
