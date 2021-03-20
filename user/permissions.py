from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user"""

    message = 'No tienes permisos para acceder a este recurso'

    def has_object_permission(self, request, view, obj):

        return request.user == obj
