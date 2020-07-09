from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from apps.orders.models import Order
from apps.orders.serializers import SimpleOrderSerializer


class OrderGenericView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = SimpleOrderSerializer
    permission_classes = (permissions.AllowAny,)
