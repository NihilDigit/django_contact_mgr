# Generated by Django 5.1 on 2024-08-31 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_blacklisted',
            field=models.BooleanField(default=False),
        ),
    ]
