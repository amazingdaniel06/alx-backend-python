from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'created_at'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_username',
            'conversation', 'message_body', 'sent_at'
        ]

    def get_sender_username(self, obj):
        return obj.sender.username


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'participant_count', 'messages', 'created_at'
        ]

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return value
