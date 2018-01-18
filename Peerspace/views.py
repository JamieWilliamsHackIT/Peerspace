# Standard imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
