# Standard imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# Import any models
from . import models

# This class abstracts the UserCreationForm class, this allows me to customise
# the Django signup form
class UserCreateForm(UserCreationForm):
    # The meta class holds information...
    class Meta:
        # Define the fields that the form should hold
        fields = (
            'name',
            'email',
            'password1',
            'password2',
        )
        # This gets the user model from settings.AUTH_USER_MODEL
        model = get_user_model()
    # This method runs when the object is instantiated
    def __init__(self, *args, **kwargs):
        # Run the __init__ method on the base class we inherited from with the
        # arguments and key-word arguments supplied
        super().__init__(*args, **kwargs)
        # Set the label of the email field to a more aesthetic value
        self.fields['email'].label = 'Email Address'


# This class deines the form used to update the users profile
class UpdateProfile(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'name',
            'email',
            'bio',
            'education',
            'work',
            'location',
            'profile_pic',
            'cover_pic',
        )
