# Generated by Django 4.2.14 on 2024-07-29 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0035_alter_medicalresult_dayspent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalresult',
            name='roomCharge',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
