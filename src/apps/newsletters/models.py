from django.db import models

from django.db.models import Index
from django.utils.translation import gettext_lazy as _


class NewsLetter(models.Model):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email', ]
        indexes = [
            Index(fields=('email',))
        ]

        verbose_name = _('Email')
        verbose_name_plural = _('Emails')
