from rest_framework import serializers
from .models import User, Conversation, Message


# --------------------------------------
# USER SERIALIZER
# --------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
        ]


# --------------------------------------
# MESSAGE SERIALIZER
# --------------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender_id",
            "message_body",
            "sent_at",
        ]


# --------------------------------------
# CONVERSATION SERIALIZER
# --------------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants_id",
            "messages",
            "created_at",
        ]
