from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from messaging.models import Message

User = get_user_model()


# ================================
# Delete User ViewSet (with signals)
# ================================
class UserAccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request):
        user = request.user
        username = user.username
        user.delete()  # triggers post_delete signal
        return Response(
            {"message": f"User {username} deleted successfully."},
            status=status.HTTP_200_OK
        )


# ================================
# Threaded Conversation View
# ================================
class ThreadView(APIView):

    def get(self, request, message_id):
        try:
            message = (
                Message.objects
                .select_related("sender", "receiver")
                .prefetch_related(
                    "replies__sender",
                    "replies__receiver",
                    "replies__replies__sender",
                    "replies__replies__receiver",
                )
                .get(id=message_id)
            )
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=404)

        data = {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "created_at": message.created_at,
            "thread": message.get_thread(),
        }

        return Response(data)


# ================================
# Unread Messages View
# ================================
class UnreadInboxView(APIView):

    def get(self, request):
        user = request.user

        unread_messages = Message.unread.unread_for(user)

        data = [
            {
                "id": msg.id,
                "sender": msg.sender.username,
                "content": msg.content,
                "created_at": msg.created_at,
            }
            for msg in unread_messages
        ]

        return Response({"unread_messages": data})
