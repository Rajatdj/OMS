# Generated by Django 4.1.2 on 2022-11-15 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_rename_invertory_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='counter_party_code',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='drawing_number',
        ),
    ]