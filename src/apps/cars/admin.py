from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from apps.cars.models import Color, CarModel, CarBrand, Car, Property


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', '_image')

    def _image(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="height: 50px">')
        return '----'
