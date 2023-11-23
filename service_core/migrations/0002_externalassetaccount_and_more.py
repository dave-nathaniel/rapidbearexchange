# Generated by Django 4.0 on 2023-09-10 17:57

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalAssetAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_account_id', models.CharField(max_length=50)),
                ('account_asset_type', models.CharField(choices=[('fiat', 'Fiat'), ('digital', 'Digital')], max_length=7)),
                ('account_authority_name', models.CharField(max_length=100)),
                ('account_authority_id', models.CharField(max_length=100)),
                ('account_common_name', models.CharField(max_length=50)),
                ('account_meta', models.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_core.customuser')),
            ],
        ),
        migrations.RemoveField(
            model_name='digitalassetbalance',
            name='digital_asset',
        ),
        migrations.RemoveField(
            model_name='digitalassetbalance',
            name='wallet',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userverification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='digital_assets',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='bvn',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='user_images/'),
        ),
        migrations.DeleteModel(
            name='CashAccount',
        ),
        migrations.DeleteModel(
            name='DigitalAsset',
        ),
        migrations.DeleteModel(
            name='DigitalAssetBalance',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.DeleteModel(
            name='UserVerification',
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.AddConstraint(
            model_name='externalassetaccount',
            constraint=models.UniqueConstraint(fields=('account_authority_id', 'user_account_id'), name='authority_identifier_unique'),
        ),
    ]