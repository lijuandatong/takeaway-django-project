# Generated by Django 4.1.7 on 2023-03-17 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('takeaway', '0006_alter_order_date_alter_orderdetail_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 17, 14, 44, 57, 348748, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 3, 17, 14, 44, 57, 348748, tzinfo=datetime.timezone.utc)),
        ),
    ]