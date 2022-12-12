from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Permission class to check only superuser can access.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        # permissions are only allowed to the owner of the object.
        return obj.user == request.user
