# Generated by Django 4.1.3 on 2022-12-07 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_day_person_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
