# Generated by Django 5.1 on 2024-09-09 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myPage', '0019_remove_reservation_user_id_reservation_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='user',
            new_name='user_id',
        ),
    ]
