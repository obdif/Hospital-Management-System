# Generated by Django 4.2.13 on 2024-07-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0023_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='assets/'),
        ),
    ]
