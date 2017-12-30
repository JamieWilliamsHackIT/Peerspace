from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from users.models import User

from . import forms
from . import models
from users.models import User
from . import serializers
from .feed import get_most_relevent

# Use this url for production
root_url = 'https://peerspace.herokuapp.com'
# Use this url for development
# root_url = 'https://127.0.0.8:8000'

class ListCreatePost(generics.ListCreateAPIView):
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostSerializer


class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


# class FeedPostList(generics.ListAPIView):
#     serializer_class = serializers.PostSerializer
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         post_ids = get_most_relevent(user_id)
#         print(post_ids)
#         queryset = models.Post.objects.filter(pk__in=post_ids)#.order_by('-created_at')
#         print(queryset)
#         return queryset


class FeedPostList(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        page_number = self.kwargs['page_number']
        page_size = 10
        slice1 = page_number * page_size
        slice2 = (page_number * page_size) + (page_size)
        post_ids = get_most_relevent(user_id)[slice1:slice2]
        print(post_ids)
        # This may not be the best way to tackle this issue, nevertheless
        # it is a working solution. The queryset was not ordered so I have
        # serialised the data from the posts myself

        data = []
        for _id in post_ids:
            post = get_object_or_404(models.Post, pk=_id)
            if post.proof_pic:
                proof_pic = post.proof_pic.url
            else:
                proof_pic = ''
            data.append(
                {
                    'id': post.id,
                    'title': post.title,
                    'description': post.description,
                    'created_at': post.created_at,
                    'days_since': post.time_since_creation,
                    'completed': post.completed,
                    'user_name': post.user.name,
                    'user_url': post.user.profile_pic.url,
                    'user': post.user.id,
                    'likes': [like.id for like in post.likes.all()],
                    'tags': post.tags,
                    'proof_description': post.proof_description,
                    'proof_pic': proof_pic,
                    'days_taken': post.days_taken,
                    'comments': [comment.id for comment in post.comments.all()],
                    'verifications': [verf.id for verf in post.verifications.all()],
                }
            )
        return Response(data)


class ProfilePostList(generics.ListAPIView):

    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = models.Post.objects.filter(user=user_id).order_by('-created_at')
        return queryset

from users.views import get_profile_images

def post_list(request):
    if request.user.is_authenticated:
        user = request.user
        profile_pictures = get_profile_images(user.id)
        number_of_posts = models.Post.objects.filter(user=user.id).count()
        return render(request, 'posts/post_list.html',
                        {
                            'user': user,
                            'profile_pictures': profile_pictures,
                            'number_of_posts': number_of_posts,
                        }
                    )
    else:
        return HttpResponseRedirect(reverse_lazy('login'))

def post_view(request, pk):
    # Check to see if the user is logged in
    if request.user.is_authenticated:
        # Get the post object for the post being viewed
        post = get_object_or_404(models.Post, pk=pk)
        # Check to see if the user owns the post
        if request.user.id == post.user_id:
            # Get the user's profile picture's url
            user_profile_pic = User.objects.filter(id=request.user.id).latest('id').profile_pic.url
            # Render the post_detail_user template
            return render(request, 'posts/post_detail_user.html',
                            {
                                'post': post,
                                'user_profile_pic': user_profile_pic,
                                'root_url': root_url,
                            }
                         )
        else:
            # If the user doesn't own the post then render the post_detail page
            return render(request, 'posts/post_detail.html',
                            {
                                'post': post,
                                'root_url': root_url,
                            }
                         )
    else:
        # If the user is not logged in then redirect them to the login page
        return HttpResponseRedirect(reverse_lazy('login'))


def post_edit(request, pk=None):
    user_posts = models.Post.objects.filter(user=request.user.id)
    instance = get_object_or_404(models.Post, pk=pk)
    if instance in user_posts:
        form = forms.UpdatePost(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'pk': pk,
            'title': instance.title,
            'description': instance.description,
            'tags': instance.tags,
            'form': form,
        }
        return render(request, 'posts/edit_post.html', context)
    else:
        return HttpResponseRedirect(instance.get_absolute_url())


def prove_post(request, pk=None):
    # Check to see if the user is logged in
    if request.user.is_authenticated:
        # Get all of the users posts
        user_posts = models.Post.objects.filter(user=request.user.id)
        # Get the post being proved
        post = get_object_or_404(models.Post, pk=pk)
        # The user is the owner of the post then go ahead and load the form
        if post in user_posts:
            form = forms.ProvePost(request.POST or None, request.FILES or None, instance=post)
            # Validate the form
            if form.is_valid():
                post = form.save(commit=False)
                # If the user has correctly proved the post then set the "days_taken" attribute to the number of days between
                # the post creation and post completion
                if post.proof_description and post.proof_pic:
                    post.days_taken = (timezone.now() - post.created_at).days
                post.save()
                return HttpResponseRedirect(post.get_absolute_url())
            context = {
                'pk': pk,
                'form': form,
            }
            return render(request, 'posts/prove_post.html', context)
        else:
            # If the user doesn't own the post then don't let them edit it and redirect them
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        # If they are not logged in redirect them to the login page
        return HttpResponseRedirect(reverse_lazy('login'))


def prove_post_delete_confirm(request, pk=None):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=pk)
        return render(request, 'posts/prove_post_delete_confirm.html', {'post': post})
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


def prove_post_delete(request, pk=None):
    if request.user.is_authenticated:
        user_posts = models.Post.objects.filter(user=request.user.id)
        post = get_object_or_404(models.Post, pk=pk)
        if post in user_posts:
            post.proof_pic.delete()
            post.proof_description = ''
            post.verifications.clear()
            post.completed = False
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy('users:profile_user')

    # This function determines whether the user is logged inr. It also makes sure
    # that only the owner of the post can edit/delete it
    def is_allowed(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    # I must overide the dispatch function to use the 'is_allowed' function
    # when the class-based-view is instantiated
    def dispatch(self, request, *args, **kwargs):
        if not self.is_allowed(request):
            return HttpResponseRedirect(self.object.get_absolute_url())
        return super(DeletePost, self).dispatch(request, *args, **kwargs)

import decimal
from users.models import UserPreferenceTag


class PostLikeAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        post = get_object_or_404(models.Post, pk=pk)
        # post_url = post.get_absolute_url()
        # Get the user object from the
        user = self.request.user

        # Initialise some variables
        liked = False
        updated = False

        # Define how much to adjust the weights by
        adjustment = 0.005

        # Transform the comma seperated list of tags into an actual list
        post_tags = post.tags.split(',')
        # Make list case-insensitive
        post_tags = [tag.lower() for tag in post_tags]

        # Get the user's tags as a queryset
        user_tags = UserPreferenceTag.objects.filter(user=user.id)
        # Create a list of the user's tag names
        user_tag_list = [tag.tag.lower() for tag in user_tags]

        # This function will add or subtract from the weight of the users tag.
        # The polarity argument will allow me to control whether it adds or
        # subtracts.
        def adjust_tag_weights(polarity):
            for tag in user_tags:
                if tag.tag.lower() in post_tags:
                    tag.weight += decimal.Decimal(adjustment * polarity)
                else:
                    tag.weight -= decimal.Decimal(adjustment * polarity)
                # Commit changes to database
                tag.save()
        # Check if the user is logged in
        if user.is_authenticated:
            # Get the tags of the liked post and increment their weights
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
                # If the user unlikes the post then reverse the weight ajdustment
                adjust_tag_weights(-1)
            else:
                post.likes.add(user)
                liked = True
                # If the user likes the post then adjust the weights
                adjust_tag_weights(1)
            # Indicate the like status has been updated
            updated = True
        else:
            # If they are not logged in then redirect them to login page
            return HttpResponseRedirect(reverse_lazy('login'))
        data = {
            'liked': liked,
            'likes': post.likes.count(),
            'updated': updated,
        }
        return Response(data)

class PostVerficationAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        post = get_object_or_404(models.Post, pk=pk)
        user = self.request.user

        # Initialise some variables
        verified_user = False
        updated = False

        # Check if the user is logged in
        if user.is_authenticated:
            if user in post.verifications.all():
                post.verifications.remove(user)
                verified_user = False
            else:
                post.verifications.add(user)
                verified_user = True
            # Indicate the like status has been updated
            updated = True
        else:
            # If they are not logged in then redirect them to login page
            return HttpResponseRedirect(reverse_lazy('login'))

        if post.verifications.count() >= 5:
            post.completed = True
            post.save()

        data = {
            'verified_user': verified_user,
            'verifications': post.verifications.count(),
            'completed': post.completed,
            'updated': updated,
        }
        return Response(data)


class ListCreateComment(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        post = get_object_or_404(models.Post, pk=post_id)
        comments = post.comments.all()
        comment_list = []
        for comment in comments:
            comment_list.append(
                {
                    'comment_id': comment.id,
                    'comment': comment.comment,
                    'user_id': comment.user.id,
                    'user_name': comment.user.name,
                    'user_pic_url': comment.user.profile_pic.url,
                }
            )
        return Response(comment_list)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = models.Comment(
                                comment=request.data['comment'],
                                user=request.user,
                            )
            comment.save()
            post_id = request.POST.get('post')
            post = get_object_or_404(models.Post, pk=post_id)
            post.comments.add(comment)
            post.save()

            # Define how much to adjust the weights by
            adjustment = 0.020

            # Transform the comma seperated list of tags into an actual list
            post_tags = post.tags.split(',')
            # Make list case-insensitive
            post_tags = [tag.lower() for tag in post_tags]

            # Get the user's tags as a queryset
            user_tags = UserPreferenceTag.objects.filter(user=request.user.id)
            # Create a list of the user's tag names
            user_tag_list = [tag.tag.lower() for tag in user_tags]

            # This function will add or subtract from the weight of the users tag.
            # The polarity argument will allow me to control whether it adds or
            # subtracts.
            def adjust_tag_weights(polarity):
                for tag in user_tags:
                    if tag.tag.lower() in post_tags:
                        tag.weight += decimal.Decimal(adjustment * polarity)
                    else:
                        tag.weight -= decimal.Decimal(adjustment * polarity)
                    # Commit changes to database
                    tag.save()

            adjust_tag_weights(1)

            self.comments = post.comments.count()

            return super(ListCreateComment, self).post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))


class DestroyViewComment(generics.RetrieveDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment =  get_object_or_404(models.Comment, pk=comment_id)
        if request.user.is_authenticated:
            if request.user.id == comment.user.id:
                return super(DestroyViewComment, self).delete(request, *args, **kwargs)
            return Response("You can't do that")
        return HttpResponseRedirect(reverse_lazy('login'))
