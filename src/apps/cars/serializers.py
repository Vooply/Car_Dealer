from rest_framework import serializers

from apps.cars.models import Car


class CarAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
