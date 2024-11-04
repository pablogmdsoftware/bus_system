# Generated by Django 5.1.2 on 2024-11-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_delete_bus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('bus_id', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('seats', models.PositiveSmallIntegerField()),
                ('seats_first_row', models.PositiveSmallIntegerField()),
                ('seats_reduced_mobility', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
