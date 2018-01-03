# Standard imports
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from rest_framework.response import Response

# Import the Message model
from . import models

# Import the User model
from users.models import User


# Render to messages page
def messages(request):
    return render(request, 'user_messages/messages.html')

class ConversationAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
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
        conversations = models.Conversation.objects.filter(users=user)[slice1:slice2]
        # Create JSON data
        data = []
        for conversation in conversations:
            user_list = []
            for user in conversation.users.all():
                if user.profile_pic:
                    profile_pic_url = user.profile_pic.url
                else:
                    profile_pic_url = '/static/default_profile_pic.svg'
                user_list.append(
                    {
                        'id'               :  user.id,
                        'name'             :  user.name,
                        'profile_pic_url'  :  profile_pic_url,
                    }
                )
            data.append(
                {
                    'id'          :  conversation.id,
                    'name'        :  conversation.name,
                    'created_at'  :  conversation.created_at,
                    'users'       :  user_list,
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
                    'id'               :  user.id,
                    'name'             :  user.name,
                    'profile_pic_url'  :  profile_pic_url,
                }
            )
        data = {
            'id'     :  conversation.id,
            'name'   :  conversation.name,
            'users'  :  user_list
        }

        return Response(data)



class MessageAPI(APIView):
    authenication_classes = (authentication.SessionAuthentication,)
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
        messages = conversation.messages.all().order_by('created_at')[slice1:slice2]
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
                    'created_at': message.created_at,
                }
            )
        return Response(data)

    def post(self, request, format=None, sender_id=None, sent_to_id=None, body=None):
        pass
