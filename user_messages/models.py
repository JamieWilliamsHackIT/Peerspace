# Standard imports
from django.db import models
from django.utils import timezone
from django.conf import settings
from channels import Group
import json

# Import User model
from users.models import User

from .settings import MSG_TYPE_MESSAGE


# Define the Message model
class Message(models.Model):
    # Define the message body
    body = models.TextField()
    # Define the ForeignKey relation
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='conversation_user', null=True)
    # Store the date and time sent
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def time_ago(self):
        return timezone.now() - self.created_at


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

    @property
    def time_ago(self):
        return timezone.now() - self.created_at

    @property
    def websocket_group(self):
        return Group('conversation-{self.id}')

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        final_msg = dict(room=str(self.id), message=message, email=user.email, msg_type=msg_type)
        self.websocket_group.send(
            {
                'text': json.dumps(final_msg),
            }
        )