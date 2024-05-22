from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('text-query/', views.TextQueryView.as_view(), name='text-query'),
]
