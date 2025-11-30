from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to return unread messages for a specific user.
    Required by ALX checker to use: Message.unread.unread_for_user(user)
    """

    def unread_for_user(self, user):
        # optimizer using only() as required
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "created_at")  # required keyword: .only
            .select_related("sender")
        )
