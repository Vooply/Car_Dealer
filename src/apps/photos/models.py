from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from common.models import BaseDateAuditModel


class Photo(BaseDateAuditModel):
    image = models.ImageField(upload_to='photos/')
    position = models.SmallIntegerField(default=1, validators=[MinValueValidator(limit_value=1)])
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='photos')

    class Meta:
        ordering = ['position']
