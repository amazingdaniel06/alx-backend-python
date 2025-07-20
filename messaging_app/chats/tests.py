from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Conversation, Message

class MessagingAppTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_conversation(self):
        url = reverse('conversation-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_message(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user)
        url = reverse('message-list')
        data = {
            "conversation": str(conversation.conversation_id),
            "message_body": "Hello world!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().message_body, "Hello world!")
