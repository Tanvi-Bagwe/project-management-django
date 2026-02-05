from django.urls import path

from .views import inbox, start_chat, get_messages, send_message

urlpatterns = [
    path("messages/", inbox, name="messages"),
    path("messages/start/", start_chat, name="start_chat"),
    path("messages/<int:conv_id>/", get_messages, name="get_messages"),
    path("messages/<int:conv_id>/send/", send_message, name="send_message"),
]
