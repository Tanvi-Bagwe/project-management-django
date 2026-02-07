from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Conversation, Message


@login_required
def inbox(request):
    # This finds any conversation where the current user is either participant 1 or 2
    conversations = Conversation.objects.filter(
        models.Q(user1=request.user) |
        models.Q(user2=request.user)
    )

    return render(request, "messages/inbox.html", {
        "conversations": conversations,
        # We need a list of other users so we can start a new chat with them
        "users": User.objects.exclude(id=request.user.id)
    })


@login_required
def start_chat(request):
    # Pull the ID from the modal dropdown
    user_id = request.POST.get("user_id")  # Using .get() is safer than ["user_id"]
    other = User.objects.get(id=user_id)

    # I sorted the users by ID so that (User A, User B) is the same
    # as (User B, User A). This prevents two separate chats for the same two people.
    user1, user2 = sorted(
        [request.user, other],
        key=lambda x: x.id
    )

    # If the chat exists, get it. If not, create it.
    conv, _ = Conversation.objects.get_or_create(
        user1=user1, user2=user2
    )

    return JsonResponse({"conversation_id": conv.id})


@login_required
def get_messages(request, conv_id):
    # Grab the conversation or fail if it's a bad ID
    conv = get_object_or_404(Conversation, id=conv_id)

    if request.user not in [conv.user1, conv.user2]:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # Pull the history and order it so newest messages are at the bottom
    messages = Message.objects.filter(conversation=conv).order_by("created_at")

    # Turn the database objects into a simple list of data for JavaScript to read
    return JsonResponse({
        "messages": [
            {
                "sender": m.sender.username,
                "content": m.content,
                # 'is_me' helps the frontend decide if the bubble goes left or right
                "is_me": m.sender == request.user,
                "time": m.created_at.strftime("%H:%M")
            }
            for m in messages
        ]
    })


@login_required
def send_message(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    # Create the new message record
    content = request.POST.get("content", "").strip()

    if content:  # Only save if there is actually text
        Message.objects.create(
            conversation=conv,
            sender=request.user,
            content=content,
            created_at=timezone.now()
        )
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Empty message"}, status=400)
