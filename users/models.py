# These imports allow me to extend/abstract the base user model.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
# Standard imports
from django.db import models
from django.utils import timezone
from django.conf import settings

from django_fields import DefaultStaticImageField

from posts.models import Post

# The user manager class controls how users and superusers are created
# It extends the base user manager that comes with Django
class UserManager(BaseUserManager):
    # This method is run when a new user is created
    def create_user(self, email, name, password):
        # Check to see if the user has provided an email.
        if not email:
            # If not then raise an error
            raise ValueError('Please provide an E-Mail address')
        # Initialise the user model
        user = self.model(
            # The normalize_email() function will make sure that all the emails
            # across the project are formatted identically
            email=self.normalize_email(email),
            name=name,
        )
        # The set_password() function manages the passwork security such as the
        # password hashing
        user.set_password(password)
        # Save the user to the database
        # Set the default profile and cover pictures
        user.save
        # Return the user
        return user

    # This method is called when a superuser is created, this will be done in
    # the command line
    def create_superuser(self, email, name, password):
        # Take the info from the create_user() method
        user = self.create_user(
            email,
            name,
            password
        )
        # Set the is_staff value to True
        user.is_staff = True
        # Set the is_superuser value to True
        user.is_superuser = True
        # Save the superuser to the database
        user.save()
        # Return the superuser
        return user

from numpy import arctan
from math import floor

# This class is my custom user model
class User(AbstractBaseUser, PermissionsMixin):
    # The users email is used as the unique identifier of their account
    email = models.EmailField(unique=True)
    # This field holds the name of the user
    # (they can decide whether to give both first and last name or ethier.)
    name = models.CharField(max_length=72, default='')
    # This field holds a short bio about the user
    bio = models.TextField(blank=True, default='')
    # This field auto fills with the time of account creation
    date_joined = models.DateTimeField(default=timezone.now)
    # This field is used to determine whether the user's account is active.
    is_active = models.BooleanField(default=True)
    # This field is used to determine whether the user is a staff user
    is_staff = models.BooleanField(default=False)
    # This field is used to hold any accounts the user is followed by
    follows = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='followed_by',
                                    default='',
                                    blank=True
                                    )
    # This field is used to hold any accounts the user sfollows
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    default='',
                                    blank=True
                                    )

    profile_pic = DefaultStaticImageField(
                                    blank=True,
                                    default='/static/default_profile_pic.svg',
                                    )

    cover_pic = models.ImageField(blank=True, null=True)

    points = models.IntegerField(default=0, blank=True, null=True)

    completion_index = models.IntegerField(default=0, blank=True, null=True)

    education = models.CharField(max_length=50, blank=True, default='')

    work = models.CharField(max_length=50, blank=True, default='')

    location = models.CharField(max_length=50, blank=True, default='')

    objects = UserManager()
    # This attribute tells Django what field to expect as the username, or
    # unique identifier for the user
    USERNAME_FIELD = 'email'
    # This attribute tells Django that the "name" field is required
    REQUIRED_FIELDS = ['name']

    @property
    def level(self):
        return (10 * arctan(self.points / 550))

    @property
    def level_floor(self):
        return floor(self.level)

    @property
    def level_percentage(self):
        return floor((self.level - floor(self.level)) * 100)



# This class holds the user's preferences
class UserPreferenceTag(models.Model):
    # The name of the tag. There cannot be more than one tag with the same name
    tag = models.CharField(max_length=100, unique=False)
    # This field is better described in the section containing the relation
    # algorithm. It holes the weight of the tag as a float
    weight = models.DecimalField(max_digits=10, decimal_places=5, default=0.5)
    # This is the foreign key that relates the user to the tag
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None)

    # This method reterns the tag name and weight when it is referenced
    def __str__(self):
        return "{}: {} for {}: {}".format(self.user.id, self.user.name, self.tag, self.weight)
