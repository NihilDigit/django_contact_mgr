# Generated by Django 5.1 on 2024-08-31 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('user_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('ct_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ct_name', models.CharField(max_length=100)),
                ('ct_phone', models.CharField(max_length=11)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.user')),
            ],
        ),
    ]
