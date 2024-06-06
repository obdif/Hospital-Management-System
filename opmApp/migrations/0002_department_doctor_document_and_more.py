# Generated by Django 4.2.13 on 2024-05-26 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='images/doctor_documents/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.FileField(default='images/profile/prfile.jpeg', upload_to='images/profile/'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opmApp.department'),
        ),
    ]
