# Generated by Django 4.0 on 2023-12-20 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_core', '0004_alter_userprofile_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='identity_verified',
        ),
    ]