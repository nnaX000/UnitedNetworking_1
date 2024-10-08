# Generated by Django 5.1 on 2024-09-08 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myPage', '0012_rename_center_name_reservation_center_data_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='credit_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class',
            name='date',
            field=models.CharField(default='Unknown Date', max_length=50),
        ),
        migrations.AddField(
            model_name='class',
            name='detail',
            field=models.CharField(default='No Details Provided', max_length=200),
        ),
        migrations.AddField(
            model_name='class',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='class',
            name='center_data_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='class',
            name='teacher',
            field=models.CharField(default='Unknown Teacher', max_length=100),
        ),
        migrations.AlterField(
            model_name='class',
            name='time',
            field=models.CharField(default='Unknown Time', max_length=50),
        ),
    ]
