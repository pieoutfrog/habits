from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Пользователь может выполнять CRUD операции только с собственными привычками."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner