# Generated by Django 4.0.3 on 2022-04-25 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BestBuySearch', '0006_vendorproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorproduct',
            name='brief_description',
            field=models.CharField(default='brief description...', max_length=20),
        ),
        migrations.AddField(
            model_name='vendorproduct',
            name='product_description',
            field=models.CharField(default='product description...', max_length=200),
        ),
    ]
