import logging

from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.cars.models import Car
from apps.newsletters.models import NewsLetter
from common.celery import app


@app.task()
def send_notification(car_id: int):
    car = Car.objects.filter(id=car_id, status=Car.STATUS_PUBLISHED).values('model')
    emails = NewsLetter.objects.all().values_list('email', flat=True)

    send_mail(subject=f'New car: {car.model}',
              message=f'Hello, we have a new car :), http://localhost:8000/cars/{car_id}',
              recipient_list=emails,
              from_email=settings.EMAIL_HOST_USER)


@periodic_task(run_every=(crontab(minute='*/10')), name='task_change_status_for_publish')
def task_change_status_for_publish():
    now = timezone.now()
    cars = Car.objects.filter(status=Car.STATUS_WAIT_FOR_PUBLISH, public_time__lte=now)
    for car in cars:
        if car.public_time <= now:
            car.status = car.STATUS_PUBLISHED
            logging.info('Success change status car')

    Car.objects.bulk_update(cars, fields=['status'])
