# Generated by Django 4.2.13 on 2024-06-02 14:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0014_remove_doctor_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='current_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
