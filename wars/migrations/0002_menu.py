# Generated by Django 4.2.9 on 2024-01-31 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_rename_restaurant_represenative_restaurant_restaurant_representative'),
        ('wars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('dishes', models.ManyToManyField(related_name='menus', to='restaurants.dish')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='restaurants.restaurant')),
                ('wars', models.ManyToManyField(related_name='menus', to='wars.war')),
            ],
        ),
    ]
