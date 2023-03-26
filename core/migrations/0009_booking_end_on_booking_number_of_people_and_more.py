# Generated by Django 4.1.3 on 2023-01-15 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_booking_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='end_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 15, 22, 3, 27, 791192, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='number_of_people',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='start_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 15, 22, 3, 44, 908055, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]