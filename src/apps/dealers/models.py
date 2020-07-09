import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.db.models import signals

from apps.dealers.managers import UserManager
from apps.dealers.tasks import send_verification_email


class Country(models.Model):
    name = models.CharField(max_length=32, unique=True)


class City(models.Model):
    name = models.CharField(max_length=32, db_index=True)
    country = models.ForeignKey(to='Country', on_delete=models.CASCADE, null=True)


class Address(models.Model):
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=128, blank=True)
    zip_code = models.PositiveSmallIntegerField()

    city = models.ForeignKey(to='City', on_delete=models.CASCADE)


class Dealer(AbstractBaseUser, PermissionsMixin):
    address = models.ForeignKey(to='Address', on_delete=models.CASCADE, null=True)

    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        send_verification_email.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=Dealer)
