# Generated by Django 4.2.5 on 2023-09-23 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('sensor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pk', to='measurement.sensor')),
            ],
        ),
    ]
