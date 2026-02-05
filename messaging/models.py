from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="conv_user1")
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="conv_user2")
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "conversations"
        unique_together = ("user1", "user2")


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "messages"
