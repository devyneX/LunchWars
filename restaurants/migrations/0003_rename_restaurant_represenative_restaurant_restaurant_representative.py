# Generated by Django 4.2.9 on 2024-01-31 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_remove_restaurant_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='restaurant_represenative',
            new_name='restaurant_representative',
        ),
    ]
