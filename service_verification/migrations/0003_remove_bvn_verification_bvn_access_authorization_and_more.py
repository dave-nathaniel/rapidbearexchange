# Generated by Django 4.0 on 2023-12-20 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_verification', '0002_bvn_verification_max_attempt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bvn_verification',
            name='bvn_access_authorization',
        ),
        migrations.AlterField(
            model_name='id_verification',
            name='review_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
