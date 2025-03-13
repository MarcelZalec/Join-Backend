from rest_framework.permissions import BasePermission, SAFE_METHODS
EXTRA_METHODS = SAFE_METHODS + ('POST', 'DELETE', 'PUT')

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_active = bool(request.user and request.user.is_active)
        return is_active or (request.method in EXTRA_METHODS)
    

class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user.is_superuser)
        else:
            bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user.is_superuser)
        else:
            return bool(request.user and request.user == obj.user)