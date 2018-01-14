import json
from django.shortcuts import get_object_or_404
from channels import Group
from channels.auth import channel_session_user_from_http
from channels.auth import channel_session_user

from .models import Conversation


@channel_session_user_from_http
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({'accept': True})
    # Add them to the right groups
    conversations = Conversation.objects.filter(users=message.user)
    for conversation in conversations:
        Group('conversation-{}'.format(conversation.id)).add(message.reply_channel)


@channel_session_user
def ws_message(message):
    # Get conversation
    conversation = get_object_or_404(Conversation, id=message['conversation_id'])
    # Get the latest message
    last_message = conversation.messages.all().order_by('-created_at')[0]
    data = {
        'message_id': last_message.id,
        'body': last_message.body,
        'user_id': last_message.user.id,
        'user_name': last_message.user.name,
        'profile_pic_url': last_message.user.profile_pic.url,
        'time_ago': last_message.time_ago.total_seconds(),
        'conversation_id': conversation.id,
    }
    Group('conversation-{}'.format(conversation.id)).send({
        'text': json.dumps(data),
    })


@channel_session_user
def ws_disconnect(message):
    # Get all the users conversations
    conversations = Conversation.objects.filter(users=message.user)
    for conversation in conversations:
        Group('conversation-{}'.format(conversation.id)).discard(message.reply_channel)