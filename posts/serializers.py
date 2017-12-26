from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):

    days_since = serializers.ReadOnlyField(source='time_since_creation')
    user_name = serializers.ReadOnlyField(source='user.name')

    try:
        user_url = serializers.ReadOnlyField(source='user.profile_pic.url')
    except:
        user_url = "/media/default_profile_pic.svg"

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
