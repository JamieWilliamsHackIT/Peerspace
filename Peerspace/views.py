from django.shortcuts import render

from users.models import User
from posts.models import Post

# Use this url for production
root_url = 'https://peerspace.herokuapp.com'
# Use this url for development
# root_url = 'https://127.0.0.8:8000'

def home_view(request):
    users = User.objects.all()
    posts = Post.objects.all()
    return render(request, 'home.html',
                    {
                        'users': users,
                        'posts': posts,
                        'root_url': root_url,
                    }
                 )
