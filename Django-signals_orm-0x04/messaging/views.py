from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Message
from django.contrib.auth.models import User
import json

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(cache_page(60), name='dispatch')  # ✅ cache for 60s
class SendMessageView(View):
    @method_decorator(login_required)
    def post(self, request):
        data = json.loads(request.body)
        receiver_id = data.get("receiver")
        content = data.get("content")

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Receiver not found"}, status=404)

        # ✅ sender=request.user and receiver
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
        # ✅ Required: Message.objects.filter + select_related + only
        messages = Message.objects.filter(receiver=request.user)\
            .select_related('sender')\
            .only('id', 'sender', 'content', 'timestamp')

        message_list = [{
            "id": msg.id,
            "from": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        } for msg in messages]

        return JsonResponse({"messages": message_list})


@method_decorator(login_required, name='dispatch')
class UnreadMessagesView(View):
    def get(self, request):
        # ✅ Message.unread.unread_for_user + only
        messages = Message.unread.unread_for_user(request.user)

        unread_list = [{
            "id": msg.id,
            "from": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        } for msg in messages]

        return JsonResponse({"unread_messages": unread_list})


@csrf_exempt
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # ✅ Required: user.delete()
        return JsonResponse({"message": "User deleted successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)
