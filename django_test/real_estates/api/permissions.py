from rest_framework.permissions import BasePermission


class IsCreatorOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:  # list or get
            return True
        if not request.user:  # not authenticated
            return False

        is_creator = obj.created_by == request.user
        is_superuser = request.user.is_superuser

        return is_creator or is_superuser
