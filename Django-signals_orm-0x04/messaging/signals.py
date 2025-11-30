from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """Create a notification when a new message is sent."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=f"You received a new message from {instance.sender.username}"
        )

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    # If instance has NO id → it is a new message → do nothing
    if not instance.pk:
        return

    # Fetch the existing stored message
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Compare old content with new content
    if old_message.content != instance.content:
        # Save old content in history
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
        )

        # Mark message as edited
        instance.edited = True

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    user = instance

    # Delete messages by user
    user_messages = Message.objects.filter(user=user)

    # Delete message history for each message
    MessageHistory.objects.filter(message__in=user_messages).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=user).delete()

    # Finally delete messages
    user_messages.delete()

    print(f"Cleaned up data for deleted user: {user.username}")
