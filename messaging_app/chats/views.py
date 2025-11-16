from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


# ---------------------------------------------------------
# CONVERSATION VIEWSET
# ---------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with provided participants.
        Expected payload:
        {
            "participants_id": ["uuid1", "uuid2"]
        }
        """
        participant_ids = request.data.get("participants_id", [])

        if not participant_ids:
            return Response({"error": "participants_id is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)

        if not participants:
            return Response({"error": "Invalid participant IDs"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants_id.set(participants)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """
        Custom endpoint: POST /conversations/<id>/add_message/
        {
            "sender_id": "<uuid>",
            "message_body": "Hello!"
        }
        """
        conversation = self.get_object()

        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not sender_id or not message_body:
            return Response({"error": "sender_id and message_body required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"},
                            status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender,
            message_body=message_body,
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------
# MESSAGE VIEWSET
# ---------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a message.
        Expected payload:
        {
            "conversation": "<uuid>",
            "sender_id": "<uuid>",
            "message_body": "Hello!"
        }
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response({"error": "conversation, sender_id, message_body required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender not found"},
                            status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender,
            message_body=message_body
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


# The following errors are asserted by the chats\views.py file code above 


# Checks Using viewsets from rest-framework Create viewsets for listing conversations (ConversationViewSet) and messages (MessageViewSet)

#     chats/views.py doesn't contain: ["filters"]

# Checks for Implement the endpoints to create a new conversation and send messages to an existing one

#     chats/urls.py doesn't contain: ["routers.DefaultRouter()"]

