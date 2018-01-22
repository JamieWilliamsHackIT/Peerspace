# Standard imports
from django.urls import path

# Import any viewsW
from . import views

# Define the namespace
app_name = 'posts'

# Define the url patterns to look for
urlpatterns = [
    # View urls
    path(
        '<int:pk>/',
        views.post_view,
        name='post_detail'
    ),
    path(
        '<int:pk>/edit/',
        views.post_edit,
        name='edit'
    ),
    path(
        '<int:pk>/delete/',
        views.DeletePost.as_view(),
        name='delete'
    ),
    path(
        '<int:pk>/prove/',
        views.prove_post,
        name='prove'
    ),
    path(
        '<int:pk>/prove/delete_confirm/',
        views.prove_post_delete_confirm,
        name='prove_delete_confirm'
    ),
    path(
        '<int:pk>/prove/delete/',
        views.prove_post_delete,
        name='prove_delete'
    ),
    path(
        '<int:pk>/progress/',
        views.add_progress,
        name='progress'
    ),
    # API urls
    path(
        'api/v1/',
        views.ListCreatePost.as_view(),
        name='API_post_list'
    ),
    path(
        'api/v1/<pk>/',
        views.RetrieveUpdateDestroyPost.as_view(),
        name='API_post_detail'
    ),
    path(
        'api/v1/<int:pk>/like/',
        views.PostLikeAPI.as_view(),
        name='API_post_like'
    ),
    path(
        'api/v1/<int:pk>/verify/',
        views.PostVerificationAPI.as_view(),
        name='API_post_verify'
    ),
    path(
        'api/v1/<int:pk>/comment/<int:page_number>/',
        views.CommentAPI.as_view(),
        name='API_post_comment'
    ),
    path(
        'api/v1/comments/<int:pk>/',
        views.DestroyViewComment.as_view(),
        name='API_post_comment_delete'
    ),
    path(
        'api/v1/<page>/<int:user_id>/<int:page_number>/',
        views.FeedPostList.as_view(),
        name='feed'
    ),
    path(
        'api/v1/<int:user_id>/proof_images/<int:page_number>/',  # Watch out for urls with similar structure
        views.PostProofImageApi.as_view(),
        name='proof_images'
    ),
    path(
        'api/v1/<int:pk>/motivate/',
        views.MotivateAPI.as_view(),
        name='motivate'
    ),
]
