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


class IsMonthOwner(BasePermission):
    """Validar que eres el dueño del mes al crear un ingreso o gasto"""
    message = 'No tienes permisos para acceder a este recurso'

    def has_permission(self, request, view):
        return view.month.user == request.user


class IsPostOwner(BasePermission):
    """Validar que eres el dueño del post"""
    message = 'No tienes permisos para acceder a este recurso'

    def has_permission(self, request, view):
        return view.get_object().author == request.user
