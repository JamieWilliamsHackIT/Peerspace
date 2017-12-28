# Standard imports
from rest_framework import serializers
# Import any models
from . import models
from posts.models import Post
# Import any serializers from other models
from posts.serializers import PostSerializer


# This class takes the data from the User model and serializes it into JSON
# (JavaScript Object Notation) ready for use in the API
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # Define the model to use
        model = models.User
        # Define which fields to output
        fields = (
            # The id field does not appear in the User model as it is an auto
            # incramenting value that the database handles for us
            'id',
            'email',
            'name',
            'bio',
            'education',
            'work',
            'location',
            'date_joined',
            'is_active',
            'is_staff',
            'posts',
            'profile_pic',
        )


class UserPreferenceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPreferenceTag
        fields = (
            'tag',
            'weight',
            'user',
        )
