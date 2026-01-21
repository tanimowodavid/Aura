from django.urls import path
from . import views

app_name = 'aura'

urlpatterns = [
    # path('', views.chat_view, name='chat'),
    # path('stream/', views.chat_stream, name='chat_stream'),
    # path('clear/', views.clear_chat, name='clear_chat'),

    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('checkin/', views.checkin_view, name='checkin'),
    path('onboarding/stream/', views.onboarding_stream, name='onboarding_stream'),
    path('checkin/stream/', views.checkin_stream, name='checkin_stream'),
]