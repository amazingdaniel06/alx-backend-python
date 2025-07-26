from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users to access the API,
    and only conversation participants to modify or view related data.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Ensure the user is a participant of the conversation for any request
        if hasattr(obj, 'conversation'):
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        # Restrict write actions to participants only
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # Allow GET, POST, etc. for participants too
        return is_participant
