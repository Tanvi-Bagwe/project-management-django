from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Conversation, Message


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        models.Q(user1=request.user) |
        models.Q(user2=request.user)
    )

    return render(request, "messages/inbox.html", {
        "conversations": conversations,
        "users": User.objects.exclude(id=request.user.id)
    })


@login_required
def start_chat(request):
    user_id = request.POST["user_id"]
    other = User.objects.get(id=user_id)

    user1, user2 = sorted(
        [request.user, other],
        key=lambda x: x.id
    )

    conv, _ = Conversation.objects.get_or_create(
        user1=user1, user2=user2
    )

    return JsonResponse({"conversation_id": conv.id})


@login_required
def get_messages(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    messages = Message.objects.filter(conversation=conv).order_by("created_at")

    return JsonResponse({
        "messages": [
            {
                "sender": m.sender.username,
                "content": m.content,
                "is_me": m.sender == request.user,
                "time": m.created_at.strftime("%H:%M")
            }
            for m in messages
        ]
    })


@login_required
def send_message(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    Message.objects.create(
        conversation=conv,
        sender=request.user,
        content=request.POST["content"],
        created_at=timezone.now()
    )

    return JsonResponse({"success": True})
