# Generated by Django 4.1.3 on 2022-12-09 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_jsonfile_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsonfile',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
