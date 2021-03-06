# Generated by Django 3.0.6 on 2020-07-08 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dealers', '0003_city_country'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='dealer',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='dealer',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='email',
            field=models.EmailField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
