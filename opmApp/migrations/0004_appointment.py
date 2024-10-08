# Generated by Django 4.2.13 on 2024-05-27 02:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0003_remove_doctor_specialist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='images/appointmens/')),
                ('describtion', models.TextField(max_length=1000)),
                ('status', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmApp.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmApp.patient')),
            ],
        ),
    ]
