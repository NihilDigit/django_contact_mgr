# Generated by Django 5.1 on 2024-08-31 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_contact_is_blacklisted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='is_blacklisted',
        ),
    ]