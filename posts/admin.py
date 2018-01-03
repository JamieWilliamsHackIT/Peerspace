# Standard imports
from django.contrib import admin

# Import Post and Comment models
from .models import Post, Comment

# Regiser models to admin
admin.site.register(Post)
admin.site.register(Comment)
