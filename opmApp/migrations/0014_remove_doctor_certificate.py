# Generated by Django 4.2.13 on 2024-05-31 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0013_alter_appointment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='certificate',
        ),
    ]
