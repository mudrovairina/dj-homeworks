from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsOwnerOrReadOnly()]

    def get_queryset(self):
        if self.action == "list":
            if isinstance(self.request.user, AnonymousUser):
                return Advertisement.objects.exclude(
                    status=AdvertisementStatusChoices.DRAFT
                )
            else:
                return Advertisement.objects.filter(
                    Q(status__in=[
                        AdvertisementStatusChoices.OPEN,
                        AdvertisementStatusChoices.CLOSED
                    ]) |
                    Q(creator=self.request.user,
                      status=AdvertisementStatusChoices.DRAFT
                      )
                )
        else:
            return Advertisement.objects.all()
