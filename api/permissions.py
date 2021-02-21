from rest_framework import permissions


class Isauthenticatedstaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return request.user.role.id in [1, 3]
        else:
            return False
