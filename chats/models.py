from django.db import models
from django.contrib.auth.models import User

import uuid

def get_default_chat():
    return [{"role": "system", "content": "You are a good assistant. Return all the result in the markdown."}]

class Chat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="deleted user", related_name="chats")
    title = models.CharField(max_length=500, null=True, blank=True)
    chats = models.JSONField(null=True, blank=True, default=get_default_chat)
    is_public = models.BooleanField(default=False)
    is_forked = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']