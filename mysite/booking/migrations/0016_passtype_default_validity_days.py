# Generated by Django 5.1.2 on 2024-11-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_alter_pass_num_travels_done_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passtype',
            name='default_validity_days',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
