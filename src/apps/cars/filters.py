from django_filters.rest_framework import FilterSet, RangeFilter

from apps.cars.models import Car


class PriceFilter(FilterSet):
    price = RangeFilter()

    class Meta:
        model = Car
        exclude = ['id', 'first_reg_data', 'extra_title', 'dealer', 'slug', 'number',
                   'views', 'public_time', 'created_at', 'updated_at', 'status']
