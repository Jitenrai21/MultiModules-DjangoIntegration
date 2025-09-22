from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tracker/', views.tracker_page, name='tracker_page'),
    path('process_frame/', views.process_frame, name='process_frame_api'),
    path('assistant/', views.voice_assistant_page, name='assistant'),
    path('initialize/', views.initialize, name='initialize'),
    path('process_command/', views.process_command, name='process_command'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/', views.chat, name='chat'),
    path('health/', views.health_check, name='health_check'),
]