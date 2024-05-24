from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('text-query/', views.TextQueryView.as_view(), name='text-query'),
    path('audio-query/', views.AudioQueryView.as_view(), name='audio-query'),
]
