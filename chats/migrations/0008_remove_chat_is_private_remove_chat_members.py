# Generated by Django 4.2.1 on 2023-05-18 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0007_alter_chat_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='is_private',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='members',
        ),
    ]
