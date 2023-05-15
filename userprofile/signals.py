from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserChatGptAPI

@receiver(post_save, sender=User)
def create_user_chatgpt_api(sender, instance, created, **kwargs):
    if created:
        UserChatGptAPI.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_chatgpt_api(sender, instance, **kwargs):
    instance.userchatgptapi.save()