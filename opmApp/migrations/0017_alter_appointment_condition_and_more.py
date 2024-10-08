# Generated by Django 4.2.13 on 2024-06-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0016_doctoravailableday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='condition',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor_note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile/prfile.jpeg', upload_to='images/profile/'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='document',
            field=models.ImageField(blank=True, null=True, upload_to='images/doctor_documents/'),
        ),
    ]
