import pytest
from rest_framework.reverse import reverse

from apps.orders.models import Order
from tests.fixtures.cars import CarFactory, OrderFactory


@pytest.mark.django_db
def test_order_create(client):
    car = CarFactory()
    data = {
        "first_name": "Tiki",
        "last_name": "Taka",
        "email": "Tik@or.com",
        "car_id ": car.id,
        "phone": "12345672121",

    }
    assert Order.objects.count() == 0
    resp = client.post(
        path=reverse('orders:create'),
        data=data
    )
    assert resp.status_code == 201
    orders = Order.objects.all()
    assert len(orders) == 1
    assert orders[0].first_name == 'Tiki'
    assert orders[0].last_name == 'Taka'
    assert orders[0].email == 'Tik@or.com'
    assert orders[0].car_id == car.id
    assert orders[0].phone == '12345672121'


@pytest.mark.django_db
def test_order_create_unique(client):
    car = CarFactory()
    OrderFactory(email='Ikra@or.ua', car=car)
    data = {
        "first_name": "Tiki",
        "last_name": "Taka",
        "email": "Ikra@or.com",
        "car": car.id,
        "phone": "12345672121",

    }

    resp = client.post(
        path=reverse('orders:create'),
        data=data
    )
    assert resp.status_code == 400
  #  assert resp.data['errors']
    assert Order.objects.count() == 1
