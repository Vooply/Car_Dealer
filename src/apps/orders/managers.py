from django.db import models


class OrderQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status='paid')

    def archived(self):
        return self.filter(status='archived')

    def pending(self):
        return self.filter(status='pending payment')

    def deposit(self):
        return self.filter(status='deposit paid')
