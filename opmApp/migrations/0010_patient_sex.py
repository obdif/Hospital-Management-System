# Generated by Django 4.2.13 on 2024-05-30 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0009_remove_appointment_image_appointment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='sex',
            field=models.CharField(default='--', max_length=10),
        ),
    ]
