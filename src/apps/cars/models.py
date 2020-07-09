from django.db import models
from django.db.models import Index
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from apps.cars.managers import CarManager, CarQuerySet
from common.models import BaseDateAuditModel


class Property(models.Model):
    category = models.CharField(max_length=50, blank=False, null=False)
    name = models.CharField(max_length=50, null=True, blank=False)

    class Meta:
        ordering = ('category',)
        indexes = [
            Index(fields=('category',))
        ]

        verbose_name = _('Property')
        verbose_name_plural = _('Properties')

    def __str__(self):
        return f'{self.category} {self.name}'


class Color(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        indexes = [
            Index(fields=('name',))
        ]

        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=32, unique=True)
    logo = models.ImageField(null=True, blank=False)

    class Meta:
        ordering = ('name',)
        indexes = [
            Index(fields=('name',))
        ]
        verbose_name = _('Car brand')
        verbose_name_plural = _('Car brands')

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=64)
    brand = models.ForeignKey('CarBrand', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        indexes = [
            Index(fields=('name',)),
        ]
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')

    def __str__(self):
        return f'{self.brand} {self.name}'


class Car(BaseDateAuditModel):
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_SOLD = 'sold'
    STATUS_ARCHIVED = 'archived'
    STATUS_WAIT_FOR_PUBLISH = 'wait for publish'

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_SOLD, "Sold"),
        (STATUS_ARCHIVED, "Archived"),
        (STATUS_WAIT_FOR_PUBLISH, 'Wait for publish'),
    )

    objects = CarManager.from_queryset(CarQuerySet)
    properties = models.ManyToManyField(Property)

    views = models.PositiveIntegerField(default=0, editable=False)
    slug = models.SlugField(max_length=75)
    number = models.CharField(max_length=16, unique=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, blank=True)

    dealer = models.ForeignKey("dealers.Dealer", on_delete=models.CASCADE, related_name='cars', null=True, blank=False)
    model = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True, blank=False)
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, null=True, blank=False)

    extra_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title second part'))

    # other fields ...
    engine_type = models.CharField(default='Rotary', max_length=15, null=False, blank=False)
    price = models.FloatField(null=True, blank=False)
    engine_power_kw = models.SmallIntegerField(null=True, blank=False)
    fuel_type = models.CharField(default='Otto', max_length=15, null=False, blank=False)
    population_type = models.CharField(max_length=15, null=True, blank=False)
    doors = models.PositiveSmallIntegerField(default=2, null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(null=True, blank=False)
    gear_case = models.SmallIntegerField(null=False, blank=True, default=1)
    sitting_place = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    first_reg_data = models.DateField(auto_now=False, auto_now_add=False, default=now)

    public_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        order_number_start = 7600000
        if not self.pk:
            super().save(*args, **kwargs)
            self.number = f"LK{order_number_start + self.pk}"
            self.save()
        else:
            super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.status = self.STATUS_ARCHIVED
        self.save()

    @property
    def title(self):
        return f'{self.model} {self.extra_title or ""}'  # do not show None

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

        indexes = [
            Index(fields=['status', ])
        ]


from apps.cars.tasks import send_notification


@receiver(models.signals.post_save, sender=Car)
def notify_by_email(sender, instance, **kwargs):
    if instance.status == Car.STATUS_PUBLISHED:
        send_notification.delay(instance.pk)
