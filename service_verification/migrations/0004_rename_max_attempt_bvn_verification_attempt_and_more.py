# Generated by Django 4.0 on 2023-12-20 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_verification', '0003_remove_bvn_verification_bvn_access_authorization_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bvn_verification',
            old_name='max_attempt',
            new_name='attempt',
        ),
        migrations.RenameField(
            model_name='id_verification',
            old_name='max_attempt',
            new_name='attempt',
        ),
    ]