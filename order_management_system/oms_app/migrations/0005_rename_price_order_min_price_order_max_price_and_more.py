# Generated by Django 4.0 on 2022-01-10 22:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("oms_app", "0004_order_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="price",
            new_name="min_price",
        ),
        migrations.AddField(
            model_name="order",
            name="max_price",
            field=models.PositiveIntegerField(default=4294967295),
        ),
        migrations.AlterField(
            model_name="order",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)
            ),
        ),
    ]