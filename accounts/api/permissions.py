from rest_framework import permissions
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework import status


class PermissionDeniedError(Exception):
    pass

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = _("Must be the owner of the account to perform this action.")

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdmin(permissions.BasePermission):
    message = _("Must be the owner of the account to perform this action.")

    def has_permission(self, request, view):
        try:
            return request.user.is_admin
        except Exception as e:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_admin
        except Exception as e:
            return False


def check_user_permissions(user, perms):
    if user.has_permissions(perms) is False:
        raise PermissionDeniedError('Permission denied')
    return True


def check_user_permission(user, perm):
    if user.has_permission(perm) is False:
        raise PermissionDeniedError('Permission denied')
    return True