from django.shortcuts import get_object_or_404
import decimal
import math

from django.shortcuts import get_object_or_404
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from users.models import User


class PostSearch(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, user_pk=None, term=None, page_size=None):
        # Take the term and return posts
        term = term.lower()

        # Get the user searching
        user = get_object_or_404(User, pk=user_pk)

        # Get all the users
        users = User.objects.all()

        # Get all the posts !!! This is not scalable
        posts = Post.objects.all()

        # Now search posts
        score_dict = {}
        for post in posts:
            post_score = 0
            if term in post.title.lower():
                post_score += 1
            if term in post.description.lower():
                post_score += 0.2
            if term in post.tags.lower():
                post_score += 2
            if term in post.user.name.lower():
                post_score += 5

            if post_score:
                post_score = decimal.Decimal(post_score)
                post_score *= decimal.Decimal(math.exp((-1 / 4) * post.time_since_creation))
                score_dict.update({post.id: post_score})
            # print('Id: {}, title: {} scored: {}'.format(post.id, post.title, post_score))

        output = {}
        sorted_score_dict = sorted(score_dict, key=score_dict.__getitem__)
        for k in sorted_score_dict:
            output.update({k: score_dict})
        post_ids = list(output.keys())
        post_ids = post_ids[::-1]

        data = []
        for id_ in post_ids[:page_size]:
            post = get_object_or_404(Post, pk=id_)
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
