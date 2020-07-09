from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
from apps.dealers.models import Dealer, Country, City, Address


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
