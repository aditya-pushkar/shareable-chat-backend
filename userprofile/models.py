from django.db import models
from django.contrib.auth.models import User

import uuid

class UserChatGptAPI(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.username