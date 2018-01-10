from django.db.models.signals import post_save
from django.dispatch import receiver

from channels import Channel

from .models import Message


@receiver(post_save, sender=Message)
def message_save_handler(sender, **kwargs):
    Channel('message_saved').send({
        'id': sender.id,
        'body': sender.body,
    })
