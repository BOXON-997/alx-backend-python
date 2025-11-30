from django.test import TestCase
from django.contrib.auth.models import User
from messaging.models import Message, Notification


class MessageNotificationTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="alice")
        self.user2 = User.objects.create(username="bob")

    def test_notification_created_when_message_sent(self):
        msg = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello Bob!"
        )

        notifications = Notification.objects.filter(user=self.user2)

        self.assertEqual(notifications.count(), 1)
        self.assertIn("alice", notifications.first().text)
