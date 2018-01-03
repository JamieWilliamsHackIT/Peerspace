# Standard imports
from django.db import models
from django.utils import timezone
from django.conf import settings

# Import the Post model
from posts.models import Post

# Define the model to hold the notification data
class Notification(models.Model):
    # This field stores the type of notification (like, comment, follow, etc...)
    _type = models.CharField(max_length=50)
    # This field holds the url of the post or user that has been liked or followed
    redirect_url = models.URLField()
    # This holds a ForeignKey relation between the notification and the recieving user
    user_rx = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name='notifications_rx')
    # This holds a ForeignKey relation between the notification and the transcieving user
    user_tx = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name='notifications_tx')
    # This holds a ForeignKey relation between the notification and a post
    post = models.ForeignKey(Post, on_delete=None, related_name='post')
    # This holds the comment data if the notification is of _type 'comment'
    comment = models.TextField(default='', blank=True)
    # This stores whether the user has seen the notification (currently not in use)
    viewed = models.BooleanField(default=False)
    # This stores the date and time when the action that created the notification was made
    created_at = models.DateTimeField(default=timezone.now)

    # This makes it easier to reference notification instances in the admin
    def __str__(self):
        return '{} notification for {}'.format(self._type, self.user_rx.name)
    # This returns the number of seconds since the notification was created
    def time_ago(self):
        return (timezone.now() - self.created_at)
