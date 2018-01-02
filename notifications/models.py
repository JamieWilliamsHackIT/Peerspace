from django.db import models
from django.utils import timezone
from django.conf import settings

from posts.models import Post

class Notification(models.Model):
    _type = models.CharField(max_length=50)

    redirect_url = models.URLField()

    user_rx = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name='notifications_rx')

    user_tx = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, related_name='notifications_tx')

    post = models.ForeignKey(Post, on_delete=None, related_name='post')

    comment = models.TextField(default='', blank=True)

    viewed = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} notification for {}'.format(self._type, self.user_rx.name)

    def time_ago(self):
        return (timezone.now() - self.created_at)
