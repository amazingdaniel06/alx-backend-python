from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter
from rest_framework.exceptions import PermissionDenied

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        if not conversation_id:
            raise PermissionDenied("conversation_id is required.")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            return Response({"detail": "Forbidden"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)

    def get_queryset(self):
        """
        Return only messages from conversations the user participates in.
        """
        return Message.objects.filter(conversation__participants=self.request.user)
