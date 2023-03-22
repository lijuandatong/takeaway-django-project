# Generated by Django 4.1.7 on 2023-03-22 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("takeaway", "0014_cartdetail_total_discount_cartdetail_total_price_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="CheckOut",),
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="order",
            name="email",
            field=models.EmailField(default="", max_length=30),
        ),
        migrations.AddField(
            model_name="order",
            name="first_name",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="order",
            name="last_name",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="order",
            name="phone",
            field=models.CharField(default="", max_length=15),
        ),
        migrations.AddField(
            model_name="order",
            name="zipcode",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 3, 22, 4, 22, 1, 417545, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
