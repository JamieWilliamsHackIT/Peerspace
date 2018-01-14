from functools import wraps
from django.shortcuts import get_object_or_404

from .exceptions import ClientError
from .models import Conversation


def catch_client_error(func):
    @wraps
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            e.send_to(message.reply_channel)
    return inner


def get_conversation_or_error(conversation_id, user):
    if not user.is_authenticated:
        raise ClientError('USER_HAS_TO_LOGIN')

    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
    except Conversation.DoesNotExist:
        raise ClientError('CONVERSATION_INVALID')
