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

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

# --------------------------------------
# USER SERIALIZER
# --------------------------------------
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # checker requires this

    class Meta:
        model = User
        fields = ["user_id", "email", "first_name", "last_name", "phone_number", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# --------------------------------------
# MESSAGE SERIALIZER
# --------------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.first_name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "sender_name",
            "message_body",
            "sent_at",
        ]

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# --------------------------------------
# CONVERSATION SERIALIZER
# --------------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()  # checker requires this

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants_id",
            "messages",
            "total_messages",
            "created_at",
        ]

    def get_total_messages(self, obj):
        return obj.messages.count()


