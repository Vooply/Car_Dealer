from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.cars.models import Car
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone', 'car')


class SimpleOrderSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=25)
    last_name = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    car_id = serializers.IntegerField()

    def validate_car_id(self, value):
        car = Car.objects.filter(id=value).last()
        if not car:
            raise serializers.ValidationError(_('Car does not exist.'))
        return car.id  # value

    def create(self, validated_data):
        return Order.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            car_id=validated_data['car_id'],

        )

    def update(self, instance, validated_data):
        pass
