# Generated by Django 4.2.9 on 2024-01-31 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='War',
            fields=[
                ('date', models.DateField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
            ],
        ),
    ]
