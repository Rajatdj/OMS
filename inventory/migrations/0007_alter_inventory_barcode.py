# Generated by Django 4.1.2 on 2022-11-21 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_inventory_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='barcode',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]
