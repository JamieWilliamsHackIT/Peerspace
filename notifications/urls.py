"""
The urls.py files in each app route http requests to views in each app's views.py
"""


# Standard imports
from django.urls import path

# Import any viewsW
from . import views

# Define the namespace
app_name = 'notifications'

# Define the url patterns to look for
urlpatterns = [
    # View urls
    # path(
    #     '<int:pk>/',
    #     views.notification_view,
    #     name='notifications'
    # ),
    # API urls
    path(
        'api/v4/<int:pk>/<int:page_number>/',
        views.NotificationAPI.as_view(),
        name='API_notifications_get'
    ),
]
