# Generated by Django 2.0.1 on 2018-01-05 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20180105_0942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='follows',
            new_name='followers',
        ),
    ]