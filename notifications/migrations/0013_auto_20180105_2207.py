# Generated by Django 2.0.1 on 2018-01-05 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0012_auto_20180105_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post', to='posts.Post'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user_rx',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications_rx', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user_tx',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications_tx', to=settings.AUTH_USER_MODEL),
        ),
    ]
