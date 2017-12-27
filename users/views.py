# Standard imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response


# Import any models
from . import models
from posts.models import Post
# Import any forms
from . import forms
# Import serializers
from . import serializers

# This class renders the signup template and form
class SignUpView(generic.CreateView):
    # Tell the view to use the custom form I created in forms.py
    form_class = forms.UserCreateForm
    # Redirect the user to the lgoin page once they've signed up
    success_url = reverse_lazy('login')
    # Tell the view what template to render
    template_name = 'users/signup.html'


# This class-based-view redirects the user to the home page rather than the
# default Django admin logout page
class LogoutView(generic.RedirectView):
    # Get the url linked the name "home"
    url = reverse_lazy('home')
    # This method logs the user out and runs the base LogoutView class using the
    # .super() method
    def get(self, request, *args, **kwargs):
        # This function takes the http request object and logs the user out
        logout(request)
        return super().get(request, *args, *kwargs)


# This class renders the page on which users can edit their profile
class UpdateProfile(LoginRequiredMixin, generic.UpdateView):
    # Set the model to the custom user model from models.py
    model = models.User
    # Set the form to the UpdateProfile form in forms.py
    form_class = forms.UpdateProfile
    # Set the redirect uel to the user's profile page
    def get_success_url(self):
        pk = self.request.user.id
        return reverse_lazy('users:profile', kwargs={'pk': pk})
    # Set the template the render
    template_name = 'users/edit_user.html'

    def get_object(self):
        return self.request.user


def update_tags_view(request):
    return render(request, 'users/edit_tags.html')


class UpdateTags(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        tags = models.UserPreferenceTag.objects.filter(user=user.id)
        tag_list = []
        for tag in tags:
            tag_list.append(tag.tag)
        data = {
            'tags': tag_list
        }
        return Response(data)

def delete_tag(request):
    tag = request.POST.get('tag')
    user = request.POST.get('user')

    models.UserPreferenceTag.objects.filter(tag=tag).filter(user=user).delete()
    data = {
    'tag': tag,
    'user': user
    }
    return Response(data)

import math
# The blocks of code within the functions appeared twice, so I refactered them
# into functions

# This function returns a dictionary of the urls of the user's latest profile picture and cover picture
def get_profile_images(user_id):
    # If the user has a profile picture then display the latest one
    user_profile_pic = models.User.objects.filter(id=user_id).latest('id').profile_pic
    if user_profile_pic:
        user_profile_pic = user_profile_pic.url
    else:
        # If not then display the default profile picutre
        user_profile_pic = '/media/default_profile_pic.svg'

    # If the user has a cover picture then display the latest one
    user_cover_pic = models.User.objects.filter(id=user_id).latest('id').cover_pic
    if user_cover_pic:
        user_cover_pic = user_cover_pic.url
    else:
        # If not then display the default cover picutre
        user_cover_pic = '/media/default_cover_pic.jpg'

    data = {
        'user_profile_pic': user_profile_pic,
        'user_cover_pic': user_cover_pic,
    }
    print(data)
    return data


def post_stats(user_id):
    posts = Post.objects.filter(user=user_id)
    number_of_posts = posts.count()
    # Calculate the user's completion percentage
    completed_posts = 0
    for post in posts:
        if post.completed:
            completed_posts += 1
    if number_of_posts:
        completion_percentage = math.floor((completed_posts / number_of_posts) * 100)
    else:
        completion_percentage = 0
    data = {
        'number_of_posts': number_of_posts,
        'completed_posts': completed_posts,
        'completion_percentage': completion_percentage,
    }
    return data


# This function-based-view renders the user's profile page
def profile_view_user(request):
    if request.user.is_authenticated:
        # Get user's information
        user = request.user

        profile_pictures = get_profile_images(user.id)

        posts = Post.objects.filter(user=user.id)

        # Render the template with the user object, profile pictures and post stats
        # in a context dictionary
        return render(request, 'users/profile_user.html', {
            'user': user,
            'profile_pictures': profile_pictures,
            'number_of_posts': post_stats(user.id)['number_of_posts'],
            'completed_posts': post_stats(user.id)['completed_posts'],
            'completion_percentage': post_stats(user.id)['completion_percentage'],
        })
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


# This function-based-view renders the user's profile page
def profile_view(request, pk):
    if request.user.is_authenticated:
        # If the user tries to "view" thier own page as if they were not logged into
        # their account then run the "logged in" view
        if request.user.id == pk:
            return profile_view_user(request)

        user = get_object_or_404(models.User, id=pk)

        profile_pictures = get_profile_images(user.id)

        if request.user in user.follows.all():
            following = True
        else:
            following = False

        # Render the template with the user object and user_profile_pic url in
        # context dictionary
        return render(request, 'users/profile.html', {
            'user': user,
            'user_viewing': request.user.id,
            'following': following,
            'profile_pictures': profile_pictures,
            'number_of_posts': post_stats(user.id)['number_of_posts'],
            'completed_posts': post_stats(user.id)['completed_posts'],
            'completion_percentage': post_stats(user.id)['completion_percentage'],
        })
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


class FollowUser(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    following = False
    updated = False

    def get(self, request, format=None, pk=None):
        following_user = request.user
        to_be_followed_user = get_object_or_404(models.User, pk=pk)

        if following_user.is_authenticated:
            if following_user in to_be_followed_user.follows.all():
                to_be_followed_user.follows.remove(following_user)
                following_user.following.remove(to_be_followed_user)
                following = False
            else:
                to_be_followed_user.follows.add(following_user)
                following_user.following.add(to_be_followed_user)
                following = True
            updated = True
        data = {
            'following': following,
            'updated': updated
        }
        return Response(data)


# These classes render the rest_framework's API views for the user
class ListCreateUser(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateDestroyUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class ListCreateUserPreferenceTag(generics.ListCreateAPIView):
    queryset = models.UserPreferenceTag.objects.all()
    serializer_class = serializers.UserPreferenceTagSerializer


class RetrieveUpdateDestroyUserPreferenceTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserPreferenceTag.objects.all()
    serializer_class = serializers.UserPreferenceTagSerializer
