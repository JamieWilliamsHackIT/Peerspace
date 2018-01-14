# Standard imports
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

# Import the User model
from users.models import User
# Import the Message model
from . import models


# Render to messages page
def messages(request, conversation_id=None):
    return render(request, 'user_messages/messages.html')


class ConversationAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # This code will run on the receipt a GET request, it will get 'pk' and
    # 'page_number' from the kwargs in the url
    def get(self, request, format=None, page_number=None):
        # Get user
        user = request.user
        # Create slices
        page_size = 10
        slice1 = (page_number * page_size)
        slice2 = (page_number * page_size) + page_size
        # Get all user's conversations
        conversations = models.Conversation.objects.filter(users=user).order_by('-created_at')[slice1:slice2]
        # Create JSON data
        data = []
        for conversation in conversations:
            display_user = {}
            for user in conversation.users.all():
                if user.profile_pic:
                    profile_pic_url = user.profile_pic.url
                else:
                    profile_pic_url = '/static/default_profile_pic.svg'
                if not user.id == request.user.id:
                    display_user = {
                        'id': user.id,
                        'name': user.name,
                        'profile_pic_url': profile_pic_url,
                    }

            data.append(
                {
                    'id': conversation.id,
                    'name': conversation.name,
                    'created_at': conversation.created_at,
                    'user': display_user,
                }
            )
        return Response(data)

    def post(self, request, *args, **kwargs):
        # Create conversation instance
        conversation = models.Conversation()
        conversation.save()
        # Get request user
        user = request.user
        # Add request user
        conversation.users.add(user)
        # Get other user(s)
        other_user = get_object_or_404(User, id=request.POST.get("other_user"))
        # Add other user
        conversation.users.add(other_user)
        # Set conversation name
        if request.POST.get('name'):
            conversation.name = request.POST.get('name')
        else:
            conversation.name = other_user.name
        # Save changes to database
        conversation.save()
        user_list = []
        for user in conversation.users.all():
            if user.profile_pic:
                profile_pic_url = user.profile_pic.url
            else:
                profile_pic_url = '/static/default_profile_pic.svg'
            user_list.append(
                {
                    'id': user.id,
                    'name': user.name,
                    'profile_pic_url': profile_pic_url,
                }
            )
        data = {
            'id': conversation.id,
            'name': conversation.name,
            'users': user_list
        }

        return Response(data)


class MessageAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # This code will run on the receipt a GET request, it will get 'pk' and
    # 'page_number' from the kwargs in the url
    def get(self, request, format=None, conversation_id=None, page_number=None):
        # Get user
        user = request.user
        # Create slices
        page_size = 10
        slice1 = (page_number * page_size)
        slice2 = (page_number * page_size) + page_size
        # Get conversation
        conversation = get_object_or_404(models.Conversation, id=conversation_id)
        # Get messages
        if not page_number:
            messages = conversation.messages.all().order_by('-created_at')[slice1:slice2][::-1]
        else:
            messages = conversation.messages.all().order_by('-created_at')[slice1:slice2]

        data = []
        for message in messages:
            if message.user.profile_pic:
                profile_pic_url = message.user.profile_pic.url
            else:
                profile_pic_url = '/static/default_profile_pic.svg'
            data.append(
                {
                    'id': message.id,
                    'body': message.body,
                    'user_id': message.user.id,
                    'user_name': message.user.name,
                    'profile_pic_url': profile_pic_url,
                    'time_ago': message.time_ago,
                }
            )

        return Response(data)

    def post(self, request, conversation_id=None, page_number=None, *args, **kwargs):
        # Get user
        user = request.user
        # Get conversation
        conversation = get_object_or_404(models.Conversation, id=conversation_id)
        # Get the message data from the POST body
        body = request.POST.get('body')
        # Add the message to the conversation instance
        # Create message instance
        message = models.Message(body=body, user=user)
        message.save()
        conversation.messages.add(message)

        if message.user.profile_pic:
            profile_pic_url = message.user.profile_pic.url
        else:
            profile_pic_url = '/static/default_profile_pic.svg'

        data = {
            'id': message.id,
            'body': message.body,
            'user_id': message.user.id,
            'user_name': message.user.name,
            'profile_pic_url': profile_pic_url,
            'time_ago': message.time_ago,
        }

        return Response(data)


class MessageRedirectAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # This code will run on the receipt a GET request, it will get 'pk' and
    # 'page_number' from the kwargs in the url
    def get(self, request, format=None, pk=None):
        # Get requesting user
        user = request.user
        # Get the other user
        other_user = get_object_or_404(User, pk=pk)

        # Get the conversation
        conversation = models.Conversation.objects.filter(users=user).filter(users=other_user)
        if conversation:
            # If a conversation between the two exists then send the id
            conversation = conversation.get()
            data = {
                'conversation_id': conversation.id,
            }
        else:
            # If no conversation between the two exists the create a new one and
            # send the id
            conversation = models.Conversation()
            conversation.save()
            conversation.users.add(user)
            conversation.users.add(other_user)
            conversation.name = other_user.name
            conversation.save()
            data = {
                'conversation_id': conversation.id,
            }

        return Response(data)
