# Standard imports
from django.db import models
from django.utils import timezone
from django.conf import settings

# Import the Post model
from posts.models import Post


class Notification(models.Model):
    """This class defines the notification model.
    When a user interacts with a post or a user the
    relevant user(s) are sent a notification letting
    them know.
    """
    _type = models.CharField(max_length=50)
    redirect_url = models.URLField()
    user_rx = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='notifications_rx',
        default=None,
        null=True
    )
    user_tx = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='notifications_tx',
        default=None,
        null=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='post',
        default=None,
        null=True
    )
    comment = models.TextField(default='', blank=True)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    progress_description = models.TextField(blank=True, null=True)
    progress_pic_url = models.URLField(blank=True, null=True)

    def __str__(self):
        """This methods makes referencing each instance in the admin easier
        """
        return '{} notification for {}'.format(self._type, self.user_rx.name)

    def time_ago(self):
        """Returns the time delta representing how long ago the notification was made
        """
        return timezone.now() - self.created_at
