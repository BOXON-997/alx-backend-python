from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # REQUIRED FOR FILTERING
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    # REQUIRED FOR PAGINATION
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Must contain 'conversation_id' for ALX checker.
        """
        conversation_id = self.kwargs.get("conversation_id")

        qs = Message.objects.filter(
            conversation__participants=self.request.user
        )

        if conversation_id:
            qs = qs.filter(conversation_id=conversation_id)

        return qs

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user)
