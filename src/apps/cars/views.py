from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.cars.models import Car
from apps.cars.permissions import CarIsAuthenticatedOrPublicOnly
from apps.cars.serializers import CarAllSerializer
from apps.dealers.models import Dealer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.filter()
    serializer_class = CarAllSerializer

    permission_classes = (CarIsAuthenticatedOrPublicOnly,)

    def public(self, request):
        queryset = self.filter_queryset(Car.objects.all())
        dealer = self.request.GET.get('delaer_id')
        if dealer is not None:
            queryset = queryset.filter(dealer_id=dealer)
        for car in queryset:
            car.views = car.views + 1
            car.save(update_fields=('views',))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def public_by_id(self, request, **kwargs):
        queryset = get_object_or_404(Car.objects.filter(pk=self.kwargs['pk']))
        queryset.views = queryset.views + 1
        queryset.save(update_fields=('views',))
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=('get',))
    def statistics(self, request):
        cars = Car.objects.filter(dealer=self.request.user).count()
        popular = Car.objects.filter(dealer=self.request.user).values().order_by('-views')[:2]
        content = [{'cars': cars}, {'two-most-popular': popular}]
        return Response(content)

    def get_queryset(self):
        return Car.objects.filter(dealer=self.request.user.id)

    def perform_create(self, serializer):
        dealer = get_object_or_404(Dealer, id=self.request.data.get('dealer'))
        return serializer.save(dealer=dealer)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        return Response(self.serializer_class(user).data)
