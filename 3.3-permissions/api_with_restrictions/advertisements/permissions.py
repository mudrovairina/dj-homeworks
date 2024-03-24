from rest_framework.permissions import BasePermission

from advertisements.models import AdvertisementStatusChoices


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return (obj.creator == request.user) or request.user.is_superuser
        elif request.method == "GET":
            if obj.status == AdvertisementStatusChoices.DRAFT:
                return obj.creator == request.user
            else:
                return True

    def has_permission(self, request, view):
        if request.method == 'POST':
            return not request.user.is_superuser
        else:
            return True
