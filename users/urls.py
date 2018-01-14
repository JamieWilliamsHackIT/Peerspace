# Standard imports
from django.urls import path

# Import views from views.py
from . import views

# Define the namespace
app_name = 'users'

# Define the url patterns to look for
urlpatterns = [
    # View urls
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'profile/',
        views.profile_view_user,
        name='profile_user'
    ),
    path(
        'edit/',
        views.UpdateProfile.as_view(),
        name='edit'
    ),
    path(
        'preferences/',
        views.update_tags_view,
        name='edit_tags'
    ),
    path(
        '<int:pk>/',
        views.profile_view,
        name='profile'
    ),
    path(
        'leaderboards/',
        views.leaderboards_view,
        name='leaderboards'
    ),
    # API urls
    path(
        'api/v2/',
        views.ListCreateUser.as_view(),
        name='users'
    ),
    path(
        'api/v2/<int:pk>',
        views.RetrieveUpdateDestroyUser.as_view(),
        name='user'
    ),
    path(
        'api/v2/<int:pk>/follow/',
        views.FollowUser.as_view(),
        name='follow'
    ),
    path(
        'api/v2/<int:pk>/followers/<_type>/<int:page_number>/',
        views.UserFollowers.as_view(),
        name='followers'
    ),
    path(
        'api/v2/suggested_users/<int:pk>/<int:page_size>/',
        views.SuggestedUsers.as_view(),
        name='suggested_users'
    ),
    path(
        'api/v2/tags/',
        views.ListCreateUserPreferenceTag.as_view(),
        name='user_tags'
    ),
    path(
        'get_preferences/',
        views.UpdateTags.as_view(),
        name='edit_tags_api'
    ),
    path(
        'api/v2/tags/<int:pk>',
        views.RetrieveUpdateDestroyUserPreferenceTag.as_view(),
        name='user_tag_detail'
    ),
    path(
        'api/v2/tags/delete/',
        views.delete_tag,
        name='delete_user_tag'
    ),
    path(
        'leaderboards/api/v3/<int:pk>/<leaderboard_group>/<leaderboard_type>/<int:page_number>/',
        views.LeaderboardsAPI.as_view(),
        name='leaderboards_API'
    ),
]
