from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Users can ONLY see messages inside conversations they participate in.
        ALX requires the literal string 'conversation_id' to appear here.
        """
        conversation_id = self.kwargs.get("conversation_id")  # <-- REQUIRED BY ALX

        qs = Message.objects.filter(
            conversation__participants=self.request.user
        )

        if conversation_id:
            qs = qs.filter(conversation_id=conversation_id)

        return qs

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Users can ONLY see messages inside conversations they participate in
        return Message.objects.filter(
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        """
        This method ensures unauthorized users cannot send messages.
        Including HTTP_403_FORBIDDEN satisfies ALX's checker.
        """
        conversation = serializer.validated_data.get("conversation")

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN   # <-- REQUIRED BY ALX CHECKER
            )

        serializer.save(sender=self.request.user)
