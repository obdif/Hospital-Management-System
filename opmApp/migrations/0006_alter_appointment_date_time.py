# Generated by Django 4.2.13 on 2024-05-27 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0005_rename_describtion_appointment_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
