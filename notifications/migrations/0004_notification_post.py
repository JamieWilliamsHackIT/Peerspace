# Generated by Django 2.0 on 2018-01-02 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_deadline'),
        ('notifications', '0003_notification_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='post',
            field=models.ForeignKey(default=None, on_delete=None, related_name='post', to='posts.Post'),
        ),
    ]
