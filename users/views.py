# Standard imports (I am aware of using commas to import multilpe things on one
# line but as I am trying to keep to PEP8 I have seperated them only their own)
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import generics
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from posts.models import Post
# Import any forms
from . import forms
# Import any models
from . import models
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


from rest_framework.decorators import api_view


@api_view(['POST'])
def delete_tag(request):
    tag = request.POST.get('tag')
    user = request.POST.get('user')

    models.UserPreferenceTag.objects.filter(tag=tag).filter(user=user).delete()

    data = {
        'tag': tag,
        'user': user,
    }

    return Response(data)


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
        user_profile_pic = '/default_profile_pic.svg'

    # If the user has a cover picture then display the latest one
    user_cover_pic = models.User.objects.filter(id=user_id).latest('id').cover_pic
    if user_cover_pic:
        user_cover_pic = user_cover_pic.url
    else:
        # If not then display the default cover picutre
        user_cover_pic = '/default_cover_pic.jpg'

    data = {
        'user_profile_pic': user_profile_pic,
        'user_cover_pic': user_cover_pic,
    }
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

    completion_index = completion_percentage * posts.count()

    data = {
        'number_of_posts': number_of_posts,
        'completed_posts': completed_posts,
        'completion_percentage': completion_percentage,
        'completion_index': completion_index,
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

        if request.user in user.followers.all():
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

        # Create a notification for the post owner
        if not following_user in to_be_followed_user.followers.all():
            notifications = Notification.objects.filter(user_tx=following_user)
            notified = False
            for notification in notifications:
                if notification.user_rx == to_be_followed_user and notification._type == 'follow':
                    notified = True
            if not notified:
                # Create notification if ine hasn't been made already
                notification = Notification()
                notification._type = 'follow'
                # I am using rx to mean receiver and tx to mean transceiver
                notification.user_rx = to_be_followed_user
                notification.user_tx = following_user
                notification.save()

        if following_user.is_authenticated:
            if following_user in to_be_followed_user.followers.all():
                to_be_followed_user.followers.remove(following_user)
                following_user.following.remove(to_be_followed_user)
                following = False
            else:
                to_be_followed_user.followers.add(following_user)
                following_user.following.add(to_be_followed_user)
                following = True
            updated = True
        data = {
            'following': following,
            'updated': updated
        }
        return Response(data)


class UserFollowers(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None, _type=None, page_number=None):
        # Get user that the profile belongs to
        user = get_object_or_404(models.User, pk=pk)
        # Get the user user viewing the page
        user_viewing = request.user
        # Set up slices
        page_size = 10
        slice1 = (page_size * page_number)
        slice2 = (page_size * page_number) + page_size
        # Get either the user's followers or the users they follow
        data = []
        if _type == 'followers':
            # Get all the user's followers
            followers = user.followers.all()[slice1:slice2]
            # For each follower determine whether the request user follows them
            for follower in followers:
                user_viewing_follow_them = False
                if follower in user_viewing.following.all():
                    user_viewing_follow_them = True

                follow_button = True
                if follower == user_viewing:
                    follow_button = False

                data.append(
                    {
                        'id': follower.id,
                        'name': follower.name,
                        'followers': follower.followers.count(),
                        'points': follower.points,
                        'profile_pic': get_profile_images(follower.id)['user_profile_pic'],
                        'user_viewing_follow_them': user_viewing_follow_them,
                        'follow_button': follow_button
                    }
                )

        elif _type == 'following':
            # Get all the users followed by the user
            following = user.following.all()[slice1:slice2]
            # Check to see if the user is on their own profile
            if not user_viewing == user:
                for follower in following:
                    user_viewing_follow_them = False
                    if follower in user_viewing.following.all():
                        user_viewing_follow_them = True

                    follow_button = True
                    if follower == user_viewing:
                        follow_button = False

                    data.append(
                        {
                            'id': follower.id,
                            'name': follower.name,
                            'followers': follower.followers.count(),
                            'points': follower.points,
                            'profile_pic': get_profile_images(follower.id)['user_profile_pic'],
                            'user_viewing_follow_them': user_viewing_follow_them,
                            'follow_button': follow_button
                        }
                    )

            else:

                for user in following:
                    data.append(
                        {
                            'id': user.id,
                            'name': user.name,
                            'followers': user.followers.count(),
                            'points': user.points,
                            'profile_pic': get_profile_images(user.id)['user_profile_pic'],
                            'follow_button': False
                        }
                    )

        return Response(data)


import math


class SuggestedUsers(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None, page_size=None):
        main_user = get_object_or_404(models.User, pk=pk)
        following = main_user.following.all()

        main_user_tags = models.UserPreferenceTag.objects.filter(user=main_user)
        main_user_tags_list = [tag.tag.lower() for tag in main_user_tags]

        score_dict = {}

        suggested_users = 0

        for user in following:
            # Get the users they follow
            user_following = user.following.all()

            for user in user_following:
                # if suggested_users <= page_size:
                if user not in main_user.following.all():
                    # Get the user's tags
                    tags = models.UserPreferenceTag.objects.filter(user=user)
                    tags = [tag.tag.lower() for tag in tags]
                    count = 0
                    score = 0
                    for tag in tags:
                        if tag in main_user_tags_list:
                            score += (1 / (1 + math.exp(-main_user_tags[count].weight)))
                        count += 1
                    score_dict.update({user.id: score})
                    # print('Id: {} and score: {}'.format(user.id, score))
                    # suggested_users += 1

        sorted_score_dict = sorted(score_dict, key=score_dict.__getitem__)
        output = {}
        for k in sorted_score_dict:
            output.update({k: score_dict})
        user_ids = list(output.keys())[::-1][:page_size]

        data = []
        for id_ in user_ids:
            user = get_object_or_404(models.User, pk=id_)
            if not user == main_user:
                data.append(
                    {
                        'id': user.id,
                        'name': user.name,
                        'profile_pic': get_profile_images(user.id)['user_profile_pic'],
                    }
                )

        return Response(data)


class TopUserAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, page_size=None):
        # Get users ordered by points
        # (Is there are way to improve this by reducing the number of db queries?)
        users = models.User.objects.all().order_by('-created_at')

        data = []
        for user in users[:page_size]:
            data.append(
                {
                    'id': user.id,
                    'name': user.name,
                    'profile_pic': get_profile_images(user.id)['user_profile_pic'],
                }
            )

        return Response(data)


def leaderboards_view(request):
    # Get users positions
    user = request.user
    points_position = list(models.User.objects.all().order_by('-points')).index(user) + 1
    users = models.User.objects.all()
    for user in users:
        user.completion_index = post_stats(user.id)['completion_index']
        user.save()
    index_position = list(models.User.objects.all().order_by('-completion_index')).index(user) + 1
    return render(request, 'users/leaderboards.html',
                  {
                      'points_position': points_position,
                      'index_position': index_position,
                      'completion_percentage': post_stats(request.user.id)['completion_percentage'],
                  }
                  )


class LeaderboardsAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None, leaderboard_group=None, leaderboard_type=None, page_number=None):
        # Get some stats
        users = models.User.objects.all()
        for user in users:
            user.completion_index = post_stats(user.id)['completion_index']
            user.save()
        # Define slices
        page_size = 10
        slice1 = (page_number * page_size)
        slice2 = (page_number * page_size) + page_size
        # Make the arguments case insensitive
        leaderboard_group = leaderboard_group.lower()
        leaderboard_type = leaderboard_type.lower()
        # Determine what type of leaderboard is being requested
        if leaderboard_group == 'global':
            if leaderboard_type == 'points':
                # Get the users and order them by their points
                results = models.User.objects.all().order_by('-points')[slice1:slice2]
            elif leaderboard_type == 'completion index':
                # Order the users by completion_index
                results = models.User.objects.all().order_by('-completion_index')[slice1:slice2]

        if leaderboard_group == 'following':
            # Get the user
            user = get_object_or_404(models.User, pk=pk)
            # Get the users they follow
            following = user.following.all() | models.User.objects.filter(id=user.id)
            if leaderboard_type == 'points':
                # Order the users by pointss
                results = following.order_by('-points')[slice1:slice2]
            elif leaderboard_type == 'completion index':
                # Order the users by completion_index
                results = following.order_by('-completion_index')[slice1:slice2]

        if leaderboard_group == '':
            # Get the user
            user = get_object_or_404(models.User, pk=pk)
            # Get the user's
            followers = user.followers.all()

            # if user.followers.all().count():
            if leaderboard_type == 'points':
                # Order users by points
                results = followers.order_by('-points')[slice1:slice2]
            elif leaderboard_type == 'completion index':
                # Order the users by completion_index
                results = followers.order_by('-completion_index')[slice1:slice2]
            # else:
            #     results = [user]

        data = []
        for user in results:
            data.append(
                {
                    'id': user.id,
                    'name': user.name,
                    'profile_pic_url': user.profile_pic.url,
                    'position': list(results).index(user) + 1,
                    'points': user.points,
                    'level': user.level_floor,
                    'completion_index': user.completion_index,
                }
            )

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
