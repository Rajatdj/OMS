# Generated by Django 4.1.2 on 2022-11-16 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_inventory_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='price',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='sku',
            field=models.CharField(max_length=200),
        ),
    ]
