from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow ONLY authenticated users
    AND only participants of the conversation to:
    - GET (view)
    - POST (send)
    - PUT (update)
    - PATCH (partial update)
    - DELETE (delete)
    messages within a conversation.
    """

    SAFE_METHODS = ["GET"]

    def has_permission(self, request, view):
        # All methods require authentication
        if not (request.user and request.user.is_authenticated):
            return False

        return True

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        - If obj is a Conversation: check participants
        - If obj is a Message: check obj.conversation.participants
        """

        # Viewing (GET)
        if request.method in ["GET"]:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        # Creating/Sending (POST)
        if request.method == "POST":
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        # Updating (PUT, PATCH)
        if request.method in ["PUT", "PATCH"]:
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        # Deleting (DELETE)
        if request.method == "DELETE":
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()

        return False
