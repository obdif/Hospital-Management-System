# Generated by Django 4.2.13 on 2024-06-04 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0015_appointment_current_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorAvailableDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=20)),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmApp.doctor')),
            ],
            options={
                'unique_together': {('doctor', 'day')},
            },
        ),
    ]
