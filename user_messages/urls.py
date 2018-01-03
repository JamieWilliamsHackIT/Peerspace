"""
The urls.py files in each app route http requests to views in each app's views.py
"""


# Standard imports
from django.urls import path

# Import any viewsW
from . import views

# Define the namespace
app_name = 'messages'

# Define the url patterns to look for
urlpatterns = [
    # View urls
    path(
        '',
        views.messages,
        name='messages'
    ),
    path(
        '<int:conversation_id>/',
        views.messages,
        name='messages_redirect'
    ),
    # API urls
    path(
        'api/v5/conversations/<int:page_number>/',
        views.ConversationAPI.as_view(),
        name='API_conversations_get'
    ),
    path(
        'api/v5/messages/<int:conversation_id>/<int:page_number>/',
        views.MessageAPI.as_view(),
        name='API_messages_get'
    ),
    path(
        'api/v5/messages/redirect/<int:pk>/',
        views.MessageRedirectAPI.as_view(),
        name='API_messages_redirect'
    ),
]
