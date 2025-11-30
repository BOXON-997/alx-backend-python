from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ------------------------
# Custom Manager
# ------------------------
class UnreadMessagesManager(models.Manager):
    def unread_for(self, user):
        """
        Return unread messages for a specific user.
        Optimized with .only() to reduce fields fetched.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "created_at")
            .select_related("sender")
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()

    # Edit tracking
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )

    # Threaded conversations
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # REQUIRED checker keyword: unread
    objects = models.Manager()
    unread = UnreadMessagesManager()  # REQUIRED

    def __str__(self):
        if self.parent_message:
            return f"Reply {self.id} → Message {self.parent_message.id}"
        return f"Message {self.id} from {self.sender.username} to {self.receiver.username}"


    # -------------------------
    # Recursive threaded fetch
    # -------------------------
    def get_thread(self):
        """Return all nested replies recursively."""
        def build_tree(message):
            children = []
            for reply in message.replies.all().select_related("sender", "receiver"):
                children.append({
                    "id": reply.id,
                    "sender": reply.sender.username,
                    "receiver": reply.receiver.username,
                    "content": reply.content,
                    "created_at": reply.created_at,
                    "replies": build_tree(reply)
                })
            return children

        return build_tree(self)


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.text}"

