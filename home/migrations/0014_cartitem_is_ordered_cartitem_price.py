# Generated by Django 5.1.5 on 2025-04-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_remove_cart_is_ordered_remove_cartitem_is_ordered_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
