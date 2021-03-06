# Standard imports
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
import decimal
from users.models import UserPreferenceTag
from notifications.models import Notification
from users.views import get_profile_images, post_stats
from notifications.models import Notification

# Import forms from app
from . import forms

# Import models from app
from . import models

# Import User model
from users.models import User

# Import serialiser from app
from . import serializers

# Import the relevance function
from .feed import get_most_relevent


# Define the list/create API view
class ListCreatePost(generics.ListCreateAPIView):
    # Define the queryset to use
    queryset = models.Post.objects.all().order_by('-created_at')
    # Define the serialiser class to use
    serializer_class = serializers.PostSerializer


# Define the list/update/delete API view
class RetrieveUpdateDestroyPost(generics.RetrieveUpdateDestroyAPIView):
    # Define the queryset to use
    queryset = models.Post.objects.all()
    # Define the serialiser class to use
    serializer_class = serializers.PostSerializer


# This API view provides the post data
class FeedPostList(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, user_id=None, page_number=None, page=None):
        page_size = 10
        posts = []
        if page == 'feed':
            post_ids = get_most_relevent(user_id, page_number, page_size)
            for _id in post_ids:
                posts.append(get_object_or_404(models.Post, id=_id))
        elif page == 'profile':
            slice1 = (page_number * page_size)
            slice2 = (page_number * page_size) + page_size
            posts = models.Post.objects.filter(user=user_id).order_by('-created_at')[slice1:slice2]
        elif page == 'detail':
            # This is a bit confusing: I needed to get the post id from the frontend and the page number parameter was
            # not being used in this case (the detail view displays only one post per page therefore the page number
            # is redundant) so I used it to get the post id.
            posts.append(get_object_or_404(models.Post, pk=page_number))

        data = []
        for post in posts:
            if post.proof_pic:
                proof_pic = post.proof_pic.url
            else:
                proof_pic = ''

            progress_data = []
            for progress in models.PostProgress.objects.filter(post=post).order_by('-created_at'):
                progress_data.append({
                    'id': progress.id,
                    'description': progress.description,
                    'progress_pic': progress.progress_pic.url,
                    'time_ago': (timezone.now() - progress.created_at).total_seconds()
                })

            data.append(
                {
                    'id': post.id,
                    'title': post.title,
                    'description': post.description,
                    'created_at': post.created_at,
                    'time_ago': post.time_since_creation,
                    'deadline': post.deadline,
                    'completed': post.completed,
                    'user_name': post.user.name,
                    'user_url': post.user.profile_pic.url,
                    'user_viewing_url': request.user.profile_pic.url,
                    'user': post.user.id,
                    'likes': [like.id for like in post.likes.all()],
                    'tags': post.tags,
                    'proof_description': post.proof_description,
                    'proof_pic': proof_pic,
                    'days_taken': post.days_taken,
                    'comments': [comment.id for comment in post.comments.all()],
                    'verifications': [verf.id for verf in post.verifications.all()],
                    'motivations': [motivation.id for motivation in post.motivations.all()],
                    'progress_updates': progress_data,
                    'page': page,
                }
            )

        return Response(data)


def post_list(request):
    # This view runs slowly only when one user has a large number of posts, the
    # time delay must come from the amount of time taken to count the number of
    # posts and calculate the post statistics for each post
    if request.user.is_authenticated:
        user = request.user
        profile_pictures = get_profile_images(user.id)
        number_of_posts = models.Post.objects.filter(user=user.id).count()
        notification_num = Notification.objects.filter(user_rx=user).count()
        if notification_num > 10:
            notification_num = '10+'
        return render(request, 'posts/post_list.html',
                      {
                          'user': user,
                          'profile_pictures': profile_pictures,
                          'number_of_posts': post_stats(user.id)['number_of_posts'],
                          'completed_posts': post_stats(user.id)['completed_posts'],
                          'completion_percentage': post_stats(user.id)['completion_percentage'],
                          'notification_num': notification_num,
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
                          }
                          )
        else:
            # If the user doesn't own the post then render the post_detail page
            return render(request, 'posts/post_detail.html',
                          {
                              'post': post,
                          }
                          )
    else:
        # If the user is not logged in then redirect them to the login page
        return HttpResponseRedirect(reverse_lazy('login'))


def post_edit(request, pk=None):
    user_posts = models.Post.objects.filter(user=request.user.id)
    instance = get_object_or_404(models.Post, pk=pk)
    if instance in user_posts:
        form = forms.UpdatePost(
            request.POST or None,
            request.FILES or None,
            instance=instance
        )

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
            form = forms.ProvePost(
                request.POST or None,
                request.FILES or None,
                instance=post
            )
            # Validate the form
            if form.is_valid():
                post = form.save(commit=False)
                # If the user has correctly proved the post then set the
                # "days_taken" attribute to the number of days between
                # the post creation and post completion
                if post.proof_description and post.proof_pic:
                    post.proved_at = timezone.now()
                    post.completed = True
                    post.save()

                    # Add points to the user
                    post_user = post.user
                    post_user.points += 50 + (2 * post.likes.count())
                    post_user.save()

                return HttpResponseRedirect(post.get_absolute_url())

            context = {
                'pk': pk,
                'form': form,
            }

            return render(request, 'posts/prove_post.html', context)
        else:
            # If the user doesn't own the post then don't let them edit it and
            # redirect them
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        # If they are not logged in redirect them to the login page
        return HttpResponseRedirect(reverse_lazy('login'))


def prove_post_delete_confirm(request, pk=None):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=pk)
        return render(request, 'posts/prove_post_delete_confirm.html',
                      {'post': post})
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
            post_user = post.user
            post_user.points -= 50
            post_user.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        return HttpResponseRedirect(reverse_lazy('login'))


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy('users:profile_user')

    # This function determines whether the user is logged inr. It also makes
    # sure that only the owner of the post can edit/delete it
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


def send_notification(_type, user, post, comment=None, progress=None):
    if _type == 'like':
        notification_group = post.likes.all()
    elif _type == 'comment':
        notification_group = []
    elif _type == 'verify':
        notification_group = post.verifications.all()
    elif _type == 'motivate':
        notification_group = post.motivations.all()
    elif _type == 'progress':
        notification_group = []
    else:
        notification_group = None

    if _type == 'progress':
        # Get all the users who have motivated the post
        for user in post.motivations.all():
            if not user == post.user:
                notification = Notification()
                notification._type = _type
                notification.redirect_url = post.get_absolute_url()
                notification.user_rx = user
                notification.user_tx = post.user
                notification.post = post
                notification.progress_description = progress.description
                notification.progress_pic_url = progress.progress_pic.url
                notification.save()

    if user not in notification_group and not user == post.user:
        notifications = Notification.objects.filter(user_tx=user)
        notified = False
        if not _type == 'comment':
            for notification in notifications:
                if notification.post == post and notification._type == _type:
                    notified = True
        else:
            if not notified:
                # Create notification if ine hasn't been made already
                notification = Notification()
                notification._type = _type
                if _type == 'comment':
                    notification.comment = comment
                notification.redirect_url = post.get_absolute_url()
                # I am using rx to mean receiver and tx to mean transceiver
                notification.user_rx = post.user
                notification.user_tx = user
                notification.post = post
                notification.save()


def add_progress(request, pk=None):
    # Check to see if the user is logged in
    if request.user.is_authenticated:
        # Get all of the users posts
        user_posts = models.Post.objects.filter(user=request.user.id)
        # Get the post being updated
        post = get_object_or_404(models.Post, pk=pk)
        # The user is the owner of the post then go ahead and load the form
        if post in user_posts:
            form = forms.PostProgress(
                request.POST or None,
                request.FILES or None,
                )
            # Validate the form
            if form.is_valid():
                post_progress = form.save(commit=False)
                if post_progress.description and post_progress.progress_pic:
                    post_progress.post = post
                    post_progress.save()

                    # Add points to the user
                    post_user = post.user
                    post_user.points += 10 + (2 * post.likes.count())
                    post_user.save()
                    send_notification('progress', request.user, post, progress=post_progress)

                return HttpResponseRedirect(post.get_absolute_url())

            context = {
                'pk': pk,
                'form': form,
            }

            return render(request, 'posts/progress.html', context)
        else:
            # If the user doesn't own the post then don't let them edit it and
            # redirect them
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        # If they are not logged in redirect them to the login page
        return HttpResponseRedirect(reverse_lazy('login'))


class PostLikeAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        post = get_object_or_404(models.Post, pk=pk)
        # post_url = post.get_absolute_url()
        # Get the user object from the
        user = self.request.user

        send_notification('like', user, post)

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
                # If the user unlikes the post reverse the weight ajdustment
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


class PostVerificationAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        # Get post
        post = get_object_or_404(models.Post, pk=pk)
        # Get user
        user = self.request.user

        send_notification('verify', user, post)

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

        data = {
            'verified_user': verified_user,
            'verifications': post.verifications.count(),
            'updated': updated,
        }
        return Response(data)


class CommentAPI(APIView, DestroyModelMixin):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Get the post Id from the url
        post_id = self.kwargs['pk']
        # Get the post object
        post = get_object_or_404(models.Post, pk=post_id)
        # Get all the comments on that post
        page_size = 5
        page_number = self.kwargs['page_number']
        slice1 = (page_number * page_size)
        slice2 = (page_number * page_size) + page_size
        comments = post.comments.all().order_by('-created_at')[slice1:slice2]
        comment_list = []
        for comment in comments:
            comment_list.append(
                {
                    'comment_id': comment.id,
                    'comment': comment.comment,
                    'user_id': comment.user.id,
                    'user_name': comment.user.name,
                    'user_pic_url': comment.user.profile_pic.url,
                    'total': post.comments.all().count(),
                }
            )

        data = {
            'comments': comment_list,
            'total': post.comments.all().count(),
        }

        return Response(data)

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

            send_notification('comment', request.user, post, comment)

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

            # This function will add or subtract from the weight of the users
            # tag. The polarity argument will allow me to control whether it
            # adds or subtracts.
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
            self.comment_id = comment.id

            data = {
                'comment_id': comment.id,
                'comment': comment.comment,
                'user_id': comment.user.id,
                'user_name': comment.user.name,
                'user_pic_url': comment.user.profile_pic.url,
                'total': post.comments.all().count(),
            }

            return Response(data)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))


class DestroyViewComment(generics.RetrieveDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(models.Comment, pk=comment_id)
        if request.user.is_authenticated:
            if request.user.id == comment.user.id:
                return super(DestroyViewComment, self).delete(
                    request,
                    *args,
                    **kwargs
                )
            return Response("You can't do that")
        return HttpResponseRedirect(reverse_lazy('login'))


class MotivateAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, pk=None):
        # Add the user to the post's motivations
        user = request.user
        post = get_object_or_404(models.Post, pk=pk)

        send_notification('motivate', user, post)

        # Check if the user is logged in
        if user.is_authenticated:
            if user in post.motivations.all():
                post.motivations.remove(user)
                motivated_user = False
            else:
                post.motivations.add(user)
                motivated_user = True
            # Indicate the like status has been updated
            updated = True
            post.save()
        else:
            # If they are not logged in then redirect them to login page
            return HttpResponseRedirect(reverse_lazy('login'))

        data = {
            'motivated_user': motivated_user,
            'motivations': post.motivations.count(),
            'updated': updated,
        }

        return Response(data)


class PostProofImageApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, user_id=None, page_number=None):
        print('get')
        # Get user
        user = get_object_or_404(User, pk=user_id)
        # Get their posts
        posts = models.Post.objects.filter(user=user).order_by('-created_at')

        page_size = 10
        slice1 = (page_size * page_number)
        slice2 = (page_size * page_number) + page_size

        # Get the picture for each post
        data = []
        for post in posts[slice1:slice2]:
            if post.completed:
                # Serialise data
                data.append(
                    {
                        'id': post.id,
                        'proof_description': post.proof_description,
                        'proof_pic_url': post.proof_pic.url,
                        'proof_pic_width': post.proof_pic.width,
                        'proof_pic_height': post.proof_pic.height,
                        'post_url': post.get_absolute_url(),
                    }
                )

        return Response(data)
