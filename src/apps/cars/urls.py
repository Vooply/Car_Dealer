from django.urls import path
from rest_framework import routers

from apps.cars.views import CarViewSet

app_name = 'cars'

router = routers.SimpleRouter()
router.register(r'my', CarViewSet)

urlpatterns = [
    path('<int:pk>/', CarViewSet.as_view({'get': 'public_by_id'})),
    path('', CarViewSet.as_view({'get': 'public'})),
] + router.urls
