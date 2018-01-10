import json

from channels import Group

from .models import Message


def message_saved(message):
    # Group('conversation').send({
    #     'text': json.dumps(message)
    # })
    print(message)


def ws_connect(message):
    Group('conversation').add(message.reply_channel)


def ws_disconnect(message):
    Group('conversation').discard(message.reply_channel)
