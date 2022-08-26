from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username == request.user.username

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == 12

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.id == request.user.id