# Generated by Django 5.1 on 2024-09-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signInUp', '0005_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='using_credit',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
