"""
The admin.py file in each app allows me to register models to the Django admin,
this is a useful backend that lets me create, update, retreive and destroy
data from all models in Peerspace.
"""


from django.contrib import admin
from .models import Notification

admin.site.register(Notification)
