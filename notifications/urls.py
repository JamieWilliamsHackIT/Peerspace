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
    #     views.post_view,
    #     name='post_detail'
    # ),
    # API urls
    path(
        'api/v4/<int:pk>/<int:page_number>',
        views.NotificationAPI.as_view(),
        name='API_notifications_get'
    ),
]
