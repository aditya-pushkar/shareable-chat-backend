from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Chat
from .serializers import ChatSerializer

# token for adi: c4a1f98e6984624687ce7f14401cbb316d4e6a1f
@api_view(['GET'])
def get_chats(request):
    try:
        user = request.user
        qr = request.query_params
        
        query = qr.get("query")

        if not query:
            return Response({"message": "please add query to the URL"}, status=status.HTTP_403_FORBIDDEN)

        if(query=="chats"):
            chat_object = Chat.objects.filter(user=user, is_forked=False)
        if(query=="fork"):
            chat_object = Chat.objects.filter(user=user, is_forked=True)

        serializer = ChatSerializer(chat_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({'message': 'something went wrong in server, please try again latter', 'error': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def chat_detail(request, chat_id):
    try:
        user = request.user

        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user != user):
            return Response({"message": "Unauthorized request"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatSerializer(chat_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_chat(request):
    try:
        user = request.user
        data = request.data
        
        title = data.get('title')
        chat_obj = Chat.objects.create(user=user, title=title)
        chat_obj.save()
        serializer = ChatSerializer(chat_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_chat(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get('chat_id')
        chats = data.get('chats')

        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)
        
        chat_obj.chats = chats
        chat_obj.save()
        return Response({"message": "chat updated"}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def share_chat_to_public(request):
    try:
        user = request.user
        data = request.data
        qr = request.query_params

        share = qr.get("share")

        chat_id = data.get('chat_id')
        
        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)

        if(share=="true"):
            chat_obj.is_public  = True
        if(share=="false"):
            chat_obj.is_public = False

        chat_obj.save()
        return Response({"message": f"chat status changed to {share}"}, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def read_public_chat(request, chat_id):
    try:
        try:
            chat_obj = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response({"message": "Public chat not found."}, status=status.HTTP_404_NOT_FOUND)

        if not chat_obj.is_public:
            return Response({"message": "You don't have permission to access this page."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatSerializer(chat_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"message": "server error"}, status=status.HTTP_400_BAD_REQUEST)


# make shared chat reusable for current user //means they can copy the shared chat and make their own
@api_view(['POST'])
def fork_chat(request):
    try:
        user = request.user
        chat_id = request.data.get('chat_id')

        try:
            chat_obj = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response({"message": "Public chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # If already folked return HTTP_226_IMUSED.
        
        if chat_obj.is_private:
            try:
                members_obj = chat_obj.members.get(id=user.id)
            except ObjectDoesNotExist:
                return Response({"message": "You don't have permission to fork this chat."}, status=status.HTTP_401_UNAUTHORIZED)

            new_chat_obj = Chat.objects.create(
                user=user, 
                title=chat_obj.title,
                chats=chat_obj.chats,
                is_forked=True
            )
            new_chat_obj.save()
            return Response({"message": "Chat Forked.", "chat_id": f"{new_chat_obj.id}"}, status=status.HTTP_201_CREATED)
        
        if chat_obj.is_public:
            new_chat_obj = Chat.objects.create(
            user=user, 
            title=chat_obj.title,
            chats=chat_obj.chats,
            is_forked=True
            )
            new_chat_obj.save()
            return Response({"message": "Chat Forked.", "chat_id": f"{new_chat_obj.id}"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Server Error", "error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        return Response({"message": "Server Error", "error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

