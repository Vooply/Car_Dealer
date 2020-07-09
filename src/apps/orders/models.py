from django.db import models

# Create your models here.
from django.db.models import Index


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SOLD = 'sold'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_SOLD, "Sold"),
        (STATUS_REJECTED, "Rejected"),
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    car = models.ForeignKey(to='cars.Car', on_delete=models.SET_NULL, null=True, related_name='orders')

    class Meta:
        indexes = [
            Index(fields=['status', ])
        ]
        unique_together = (('email', 'car'),)

    def __str__(self):
        return f'{self.status.upper()} - {self.car}'
