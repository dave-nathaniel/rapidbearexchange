# Generated by Django 4.0 on 2023-09-10 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('active', models.BooleanField(default=False)),
                ('metadata', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='BaseAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('asset_type', models.CharField(choices=[('fiat', 'Fiat'), ('digital', 'Digital')], max_length=7)),
                ('metadata', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=10, max_digits=30)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('change_direction', models.CharField(choices=[('up', 'Rising'), ('down', 'Falling')], default='up', editable=False, max_length=4)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='market', to='service_markets.asset')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='base_asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_markets.baseasset'),
        ),
    ]