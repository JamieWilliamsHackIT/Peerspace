# Standard imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy

from datetime import date

# This class defines the Comment model
class Comment(models.Model):
    # Store the time and date the comment was made
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    # Store the comment data
    comment = models.TextField()
    # Define the ForeignKey relation between the comment and the user
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                unique=False,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='post'
                            )
    # This makes referencing comment instances in the admin easier
    def __str__(self):
        return self.comment


# This class defines the Post model
class Post(models.Model):
    # The exact time at which the post was created
    created_at = models.DateTimeField(default=timezone.now)
    # The title of the posts
    title = models.CharField(max_length=255)
    # The description of the post (max_length is 140 to allow for easy
    # integration with Twitter)
    description = models.TextField()
    # Whether or not the post has been completed
    completed = models.BooleanField(default=False)
    # Store the deadline set by the user
    deadline = models.DateField(default=None, null=True, blank=True)
    # The User is the foreign key (one post can belong to one user,
    # one user can have many posts)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                unique=False,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='posts'
                            )
    # Store any users that like the post
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    # Store the post's tags as a string (comma-seperated list)
    tags = models.TextField(null=True, blank=True)
    # Store the text supporting the post proof
    proof_description = models.TextField(blank=True, null=True, default=None)
    # Store the picture proving the post
    proof_pic = models.ImageField(blank=True, null=True, default=None)
    # Store the users that verified the post proof
    verifications = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='verfs')
    # Store the number of days taken to submit proof
    days_taken = models.IntegerField(blank=True, default=None, null=True)
    # Store the comments made on the post
    comments = models.ManyToManyField(Comment, blank=True, related_name='comments')

    # This will overide the __str__ method so when it is referred to it is
    # in a readable form
    def __str__(self):
        return 'Id:{}, {} by: {}'.format(self.id, self.title, self.user)

    # Get the name of the user who created the post
    @property
    def get_user(self):
        return user.name

    # This will return the number of days since the post was created
    @property
    def time_since_creation(self):
        return (timezone.now() - self.created_at).total_seconds()

    # This will return the absolute url of the post
    def get_absolute_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk':self.id})

    # Check whether the post is verified (not currently in use)
    @property
    def is_verified(self):
        if self.verifications >= 5:
            return True
        return False

    @property
    def days_to_go(self):
        # The number of days to go
        return (self.deadline - date.today()).days

    @property
    def days_to_go_percentage(self):
        # The percentage of the time left
        total_days = (self.deadline - self.created_at.date()).days
        if total_days:
            return round(self.days_to_go / (total_days * 100))
        else:
            return 0
