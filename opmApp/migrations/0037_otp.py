# Generated by Django 4.2.14 on 2024-07-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0036_alter_medicalresult_roomcharge'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(editable=False, max_length=6, unique=True)),
            ],
        ),
    ]
