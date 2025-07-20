from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Optional Nested Router
# from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]

# Optional Nested Router Example (for deeper nesting, like messages under conversation)
# nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
# nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')
#
# urlpatterns += nested_router.urls
