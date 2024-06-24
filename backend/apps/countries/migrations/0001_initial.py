# Generated by Django 5.0.6 on 2024-06-22 04:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=3, unique=True)),
                ('country_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TravelExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('cost', models.IntegerField()),
                ('sightseeing', models.CharField(max_length=100)),
                ('visited_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_user', to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='VisitedCountries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visited_countries_user', to='users.users')),
            ],
        ),
    ]
