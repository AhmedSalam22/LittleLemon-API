from rest_framework import permissions


class MangerMofidyOrReadOnly(permissions.BasePermission):
     def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated) and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name="Manger").exists()

class MangerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and request.user.groups.filter(name="Manger").exists()