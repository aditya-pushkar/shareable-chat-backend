from django.urls import path

from .views import get_chats, chat_detail,  create_chat, update_chat, share_chat_to_public, read_public_chat, fork_chat

urlpatterns = [
    path('list/', get_chats),
    path('detail/<str:chat_id>/', chat_detail),
    path('create/', create_chat),
    path('update/', update_chat),
    path('share', share_chat_to_public),
    path('read/<str:chat_id>/', read_public_chat),
    path('fork/', fork_chat),
]
