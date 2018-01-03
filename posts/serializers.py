# Standard imports
from rest_framework import serializers

# Import models from app
from . import models

# This tells the rest framework how to serialise the post model
class PostSerializer(serializers.ModelSerializer):

    # Get some extra bits of data
    days_since = serializers.ReadOnlyField(source='time_since_creation')
    user_name = serializers.ReadOnlyField(source='user.name')

    # Callig the .url method on a NoneType will result in an error, if so catch
    # the error and set the url to the default profile picture's url
    try:
        user_url = serializers.ReadOnlyField(source='user.profile_pic.url')
    except:
        user_url = "/media/default_profile_pic.svg"

    # Tell the serialiser what fields to include and what model to serialise
    class Meta:
        model = models.Post
        fields = (
            'id',
            'title',
            'description',
            'created_at',
            'days_since',
            'completed',
            'user_name',
            'user_url',
            'user',
            'likes',
            'tags',
            'proof_description',
            'proof_pic',
            'days_taken',
            'comments',
            'verifications',
        )


# Same as the previous serialiser really
class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=False, read_only=True)
    class Meta:
        model = models.Comment
        fields = (
            'id',
            'comment',
            'user',
            'post',
        )
