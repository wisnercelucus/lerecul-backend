# Generated by Django 4.1.3 on 2023-01-15 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=2500, null=True, unique=True),
        ),
    ]