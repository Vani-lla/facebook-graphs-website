# Generated by Django 4.1.3 on 2022-12-08 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_remove_messages_day_messages_date_delete_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='media',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='messages',
            name='unsend',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateField(default=0),
        ),
        migrations.AlterField(
            model_name='messages',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]