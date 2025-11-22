from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsConversationParticipant(BasePermission):
    """
    Allow access only if the user is part of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj should be a Conversation instance
        return request.user in obj.participants.all()


class IsMessageParticipant(BasePermission):
    """
    Allow viewing messages only if user is in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj should be a Message instance
        return request.user in obj.conversation.participants.all()

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow ONLY authenticated users
    AND only participants of the conversation to send,
    view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated to access ANY endpoint
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        - If obj is a Conversation → check participants
        - If obj is a Message → check obj.conversation.participants
        """
        # Handle Conversation object
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Handle Message object
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
