# Generated by Django 5.1 on 2024-09-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myPage', '0007_alter_userprofile_remaining_credit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='using_credit',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
