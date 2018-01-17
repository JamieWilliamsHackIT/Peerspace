# Standard imports
from datetime import date

from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone


class Comment(models.Model):
    """This models holds each comment
    """
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             unique=False,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='post'
                             )

    def __str__(self):
        """Returns the comment itself when the the models is referenced
        """
        return self.comment


class Post(models.Model):
    """This model holds all the information relevant to each post and the post's proof
    """
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    deadline = models.DateField(default=None, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             unique=False,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name='posts'
                             )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    tags = models.TextField(null=True, blank=True)
    proof_description = models.TextField(blank=True, null=True, default=None)
    proof_pic = models.ImageField(blank=True, null=True, default=None)
    proved_at = models.DateTimeField(default=None, blank=True, null=True)
    verifications = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='verfs')
    comments = models.ManyToManyField(Comment, blank=True, related_name='comments')

    def __str__(self):
        """Return the Id, post title, and post user
        """
        return 'Id:{}, {} by: {}'.format(self.id, self.title, self.user)

    @property
    def get_user(self):
        """Return the name of the user who the post belongs to
        """
        return self.user.name

    @property
    def time_since_creation(self):
        """Returns the total seconds of the difference between now and when the post was made
        """
        return (timezone.now() - self.created_at).total_seconds()

    def get_absolute_url(self):
        """Returns the absolute url of the post
        """
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.id})

    @property
    def days_taken(self):
        """Returns the number of days between post creation and proof submission
        """
        if self.proved_at:
            return (self.proved_at - self.created_at).days
        else:
            return 0

    @property
    def days_to_go(self):
        """Returns the number of days until the deadline
        """
        return (self.deadline - date.today()).days

    @property
    def days_to_go_percentage(self):
        """Returns the percentage of the time left
        """
        total_days = (self.deadline - self.created_at.date()).days
        if total_days:
            return round((self.days_to_go / total_days) * 100)
        else:
            return 0


class PostProgress(models.Model):
    """Model storing any post progress updates
    """
    description = models.TextField()
    progress_pic = models.ImageField(blank=True, null=True, default=None)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
