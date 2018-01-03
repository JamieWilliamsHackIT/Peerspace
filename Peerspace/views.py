# Standard imports
from django.shortcuts import render

# Import User and Post models
from users.models import User
from posts.models import Post

# Simple function-based-view that renders the home page
def home_view(request):
    users = User.objects.all()
    posts = Post.objects.all()
    return render(request, 'home.html',
                    {
                        'users': users,
                        'posts': posts,
                    }
                 )


# Simple function-based-view that renders the docs page
def docs_view(request):
    users = User.objects.all()
    posts = Post.objects.all()
    return render(request, 'docs.html',
                    {
                        'users': users,
                        'posts': posts,
                    }
                 )
