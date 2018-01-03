# Standard imports
from django import forms

# Import models
from . import models

# This defines the form for editting a post
class UpdatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = (
            'title',
            'description',
            'tags',
        )

# This defines the form for submission of post proof
class ProvePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = {
            'proof_pic',
            'proof_description',
        }
