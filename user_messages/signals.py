from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from channels import Channel

from .models import Message
from .models import Conversation


@receiver(m2m_changed, sender=Conversation.messages.through)
def message_added(instance, action, sender, **kwargs):
    if action == "post_add":
        Channel('websocket.receive').send({
            'conversation_id': instance.id,
            'reply_channel': 'websocket.receive'
        })
