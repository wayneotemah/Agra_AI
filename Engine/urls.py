from django.urls import path
from . import views

urlpatterns = [
    path('text-query/', views.TextQueryView.as_view(), name='text-query'),
    path('audio-query/', views.AudioQueryView.as_view(), name='audio-query'),
]
