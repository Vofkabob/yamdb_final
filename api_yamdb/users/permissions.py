from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """
    Требование прав администратора на все операции.
    """
    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return request.user.is_admin

        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Требование прав администратора для операций записи.
    """
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.is_admin

        return False


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    """
    Требование прав администратора, либо статуса автора для операций изменения.
    """
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_admin or request.user.is_moderator:
            return True

        if request.method in ['PATCH', 'DELETE']:
            return obj.author == request.user

        return request.user.is_authenticated
