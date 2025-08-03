from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Message
from django.contrib.auth.models import User
import json

@method_decorator(csrf_exempt, name='dispatch')
class SendMessageView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        receiver_id = data.get("receiver")
        content = data.get("content")

          messages = Message.unread.unread_for_user(request.user)

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Receiver not found"}, status=404)

        # ✅ Required: sender=request.user and receiver
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )

        return JsonResponse({
            "message": "Message sent",
            "id": message.id,
            "timestamp": message.timestamp
        })


@method_decorator(login_required, name='dispatch')
class ConversationView(View):
    def get(self, request):
        # ✅ Required: Message.objects.filter and select_related
        messages = Message.objects.filter(receiver=request.user).select_related('sender')

        message_list = [{
            "id": msg.id,
            "from": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        } for msg in messages]

        return JsonResponse({"messages": message_list})
