"""The notification app is currently at a very early stage. In the future
I plan to use Django Channels to build an ASGI (asynchronus server gate interface)
system that uses web sockets, this will mean that notifications, messages and
other actions can be displayed in real time without the need for a refresh or
continuous AJAX requests.
"""

from django.shortcuts import get_object_or_404
from rest_framework import authentication
# Standard imports
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# Import the User model
from users.models import User
# Import the Notification model
from . import models


# This class will return notification objects
class NotificationAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # This code will run on the receipt a GET request, it will get 'pk' and
    # 'page_number' from the kwargs in the url
    def get(self, request, format=None, pk=None, page_number=None):
        # Get the user
        user = get_object_or_404(User, pk=pk)
        # Define the number of notifications to return
        page_size = 10
        # Form slices (this helps reduce the number of hits on the database and
        # should improve performance).
        slice1 = (page_number * page_size)
        slice2 = (page_number * page_size) + page_size
        # Get notifications
        notifications = models.Notification.objects.filter(user_rx=user).order_by('-created_at')[slice1:slice2]
        # Send notifications as response
        data = []
        # Iterate through the notifications and create JSON data
        for notification in notifications:
            # Get the transceiving user's profile picture
            if notification.user_tx.profile_pic:
                user_tx_pic_url = notification.user_tx.profile_pic.url
            else:
                user_tx_pic_url = '/default_profile_pic.svg'

            if notification.post:
                # Create the list of objects (JSON)
                data.append(
                    {
                        # Notification info
                        'id': notification.id,
                        'type': notification._type,
                        'redirect_url': notification.redirect_url,
                        'viewed': notification.viewed,
                        'time_ago': notification.time_ago(),
                        # User info
                        'user_rx_id': notification.user_rx.id,
                        'user_rx_name': notification.user_rx.name,
                        'user_tx_id': notification.user_tx.id,
                        'user_tx_name': notification.user_tx.name,
                        'user_tx_pic_url': user_tx_pic_url,
                        # Post info
                        'post_id': notification.post.id,
                        'post_title': notification.post.title,
                        'comment': notification.comment,
                        'progress_description': notification.progress_description,
                        'progress_pic_url': notification.progress_pic_url,
                    }
                )
            else:
                # Create the list of objects (JSON)
                data.append(
                    {
                        # Notification info
                        'id': notification.id,
                        'type': notification._type,
                        'redirect_url': notification.redirect_url,
                        'viewed': notification.viewed,
                        'time_ago': notification.time_ago(),
                        # User info
                        'user_rx_id': notification.user_rx.id,
                        'user_rx_name': notification.user_rx.name,
                        'user_tx_id': notification.user_tx.id,
                        'user_tx_name': notification.user_tx.name,
                        'user_tx_pic_url': user_tx_pic_url,
                    }
                )

        # Return a HTTP response with the JSON data in the body
        return Response(data)
