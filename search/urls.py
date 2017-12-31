# Standard imports
from django.urls import path

# Import views from views.py
from . import views

# Define the namespace
app_name = 'search'

# Define the url patterns to look for
urlpatterns = [
    # View urls
    path(
        '<int:user_pk>/<term>/<int:page_size>',
        views.PostSearch.as_view(),
        name='search'
    ),
]
