# Generated by Django 3.0.6 on 2020-07-09 13:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0007_auto_20200708_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
        migrations.AddField(
            model_name='dealer',
            name='verification_uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='Unique Verification UUID'),
        ),
    ]
