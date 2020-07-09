from rest_framework.permissions import BasePermission


class CarIsAuthenticatedOrPublicOnly(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'public' or view.action == 'public_by_id':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.dealer
