# Generated by Django 5.1.2 on 2024-11-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0014_alter_bus_seats_first_row_alter_travel_bus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pass',
            name='num_travels_done',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pass',
            name='num_travels_uncompleted',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
