from django.shortcuts import render

from users.models import User
from posts.models import Post

def home_view(request):
    users = User.objects.all()
    posts = Post.objects.all()
    return render(request, 'home.html', {'users': users, 'posts': posts})
