# Standard imports
from django.contrib import admin

# Import Conversation and Message models
from . import models

admin.site.register(models.Conversation)
admin.site.register(models.Message)
