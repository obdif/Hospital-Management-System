# Generated by Django 4.2.13 on 2024-05-30 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0008_medicalresult_appointment_doctor_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='image',
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date_time',
            field=models.DateField(),
        ),
    ]
