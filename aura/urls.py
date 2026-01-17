from django.urls import path
from . import views

app_name = 'aura'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('stream/', views.chat_stream, name='chat_stream'),
    path('clear/', views.clear_chat, name='clear_chat'),
]