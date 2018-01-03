# Standard imports
from django.db import models
from django.utils import timezone
from django.conf import settings

# Import User model
from users.models import User

# Define the Message model
class Message(models.Model):
    # Define the message body
    body = models.TextField()
    # Define the ForeignKey relation
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name='conversation_user')
    # Store the date and time sent
    created_at = models.DateTimeField(default=timezone.now)

# Define the Conversation model
class Conversation(models.Model):
    # Conversation name
    name = models.CharField(max_length=24)
    # Users in the conversation
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sender')
    # Define the ManyToMany relation with the Message model
    messages = models.ManyToManyField(Message, blank=True, related_name='messages')
    # Define when the conversation started
    created_at = models.DateTimeField(default=timezone.now)
