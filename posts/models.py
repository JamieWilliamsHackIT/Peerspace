# Standard imports
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy


class Comment(models.Model):
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                unique=False,
                                null=True,
                                on_delete=None,
                                related_name='post'
                            )

    def __str__(self):
        return self.comment

# This class defines the Post model
class Post(models.Model):
    # The exact time at which the post was created
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    # The title of the posts
    title = models.CharField(max_length=255)
    # The description of the post (max_length is 140 to allow for easy
    # integration with Twitter)
    description = models.TextField()
    # Whether or not the post has been completed
    completed = models.BooleanField(default=False)
    # The User is the foreign key (one post can belong to one user,
    # one user can have many posts)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                unique=False,
                                null=True,
                                on_delete=None,
                                related_name='posts'
                            )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')

    tags = models.TextField(null=True, blank=True)

    # deadline = models.DateField(blank=True, default=None)

    proof_description = models.TextField(blank=True, null=True, default=None)

    proof_pic = models.ImageField(blank=True, null=True, default=None)

    verifications = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='verfs')

    days_taken = models.IntegerField(blank=True, default=None, null=True)

    comments = models.ManyToManyField(Comment, blank=True, related_name='comments')

    # This will overide the __str__ method so when it is referred to it is
    # in a readable form
    def __str__(self):
        return 'Id:{}, {} by: {}'.format(self.id, self.title, self.user)

    def get_user(self):
        return user.name
    # This will return the number of days since the post was created
    @property
    def time_since_creation(self):
        return (timezone.now() - self.created_at).days

    def get_absolute_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk':self.id})

    def is_verified(self):
        if self.verifications >= 5:
            return True
        return False
