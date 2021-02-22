from rest_framework import permissions


class Isauthenticatedstaff(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        permission for all the api list, post, update views, get.

        :param request:
        :param view:
        :return: bool
        """
        return bool(request.user and request.user.is_staff and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        Provides the object level permissions in api with list, update views, get views

        :param request:
        :param view:
        :param obj:
        :return: bool
        """

        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return bool(set([role.id for role in request.user.roles.all()]).intersection([1, 3]))
        else:
            return False
