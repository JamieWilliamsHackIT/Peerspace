from django import forms
from . import models


class UpdatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = (
            'title',
            'description',
            'tags',
        )


class ProvePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = {
            'proof_pic',
            'proof_description',
        }
