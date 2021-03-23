from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):

    message = 'No tienes permisos para acceder a este recurso'

    def has_permission(self, request, view):
        month = view.get_object()
        return month.user == request.user


class IsAmountBaseOwner(BasePermission):
    message = 'No tienes permisos para acceder a este recurso'

    def has_permission(self, request, view):
        amount_base = view.get_object()
        return amount_base.month.user == request.user
