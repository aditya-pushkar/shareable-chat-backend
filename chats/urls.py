from django.urls import path

from .views import get_chats, create_chat, update_chat, share_chat_to_public, share_chat_to_private, add_member_to_private_chat, read_public_chat, read_private_chat

urlpatterns = [
    path('list/', get_chats),
    path('create/', create_chat),
    path('update/', update_chat),
    path('share-to-public/', share_chat_to_public),
    path('share-to-private/', share_chat_to_private),
    path('add-member/', add_member_to_private_chat),
    path('read-public/<str:chat_id>/', read_public_chat),
    path('read-private/<str:chat_id>/', read_private_chat),
]
