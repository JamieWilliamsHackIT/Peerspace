# Generated by Django 2.0.1 on 2018-01-04 20:34

from django.db import migrations
import django_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20180104_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=django_fields.fields.DefaultStaticImageField(blank=True, default='/default_profile_pic.svg', upload_to=''),
        ),
    ]
