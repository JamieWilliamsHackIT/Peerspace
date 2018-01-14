from channels.routing import route

from user_messages.consumers import ws_message
from user_messages.consumers import ws_add
from user_messages.consumers import ws_disconnect


def message_handler(message):
    print(message['text'])


channel_routing = [
    route('websocket.receive', ws_message),
    route('websocket.connect', ws_add),
    route('websocket.disconnect', ws_disconnect),
]
