from channels.routing import route

from user_messages.consumers import message_saved
from user_messages.consumers import ws_connect
from user_messages.consumers import ws_disconnect



channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('message_saved', message_saved),
]
