from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user  # Fixed typo here
