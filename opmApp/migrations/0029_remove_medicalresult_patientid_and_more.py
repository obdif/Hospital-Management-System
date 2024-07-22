# Generated by Django 4.2.14 on 2024-07-20 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmApp', '0028_alter_medicalresult_recordnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalresult',
            name='patientId',
        ),
        migrations.AddField(
            model_name='medicalresult',
            name='invoice_id',
            field=models.CharField(default='', editable=False, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='OtherCharge',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='address',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='assignedDoctorName',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='condition_after',
            field=models.TextField(default='Good Health'),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='condition_before',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='daySpent',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='dischargeInstructions',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='dischargeMeditations',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='doctorFee',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='medicineCost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='mobile',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='patientName',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='recordNumber',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='roomCharge',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='medicalresult',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
