from django.urls import path

from apps.orders.views import OrderGenericView

app_name = 'orders'

urlpatterns = [
    path('', OrderGenericView.as_view(), name='create'),
]
