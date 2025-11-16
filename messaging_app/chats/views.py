from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()


# ---------------------------------------------------------
# Conversation ViewSet
# ---------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Listing conversations
    - Creating conversations with participants
    - Retrieving a conversation with nested messages
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Expected payload:
            {
                "participants": ["uuid1", "uuid2", ...]
            }
        """
        participant_ids = request.data.get("participants", [])

        if not participant_ids:
            return Response(
                {"error": "At least one participant is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(id__in=participant_ids)

        if not participants.exists():
            return Response(
                {"error": "Invalid participant IDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """
        Custom endpoint: POST /conversations/<id>/add_message/
        Payload:
        {
            "message_body": "Hello there"
        }
        """
        conversation = self.get_object()
        message_body = request.data.get("message_body")

        if not message_body:
            return Response(
                {"error": "message_body is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------
# Message ViewSet
# ---------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - Listing all messages
    - Creating a message inside an existing conversation
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a message.
        Expected payload:
            {
                "conversation": "<conversation_uuid>",
                "message_body": "Hello!"
            }
        """
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
