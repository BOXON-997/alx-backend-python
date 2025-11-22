from rest_framework.permissions import BasePermission

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
