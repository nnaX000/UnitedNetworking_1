# Generated by Django 5.1 on 2024-09-12 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myPage', '0024_alter_reservation_center_name_alter_reservation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='center_image_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
