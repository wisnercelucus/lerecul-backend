# Generated by Django 4.1.3 on 2023-01-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_banner_default_gallery_default_kitchen_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='in_slider',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='service',
            name='in_slider',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='strength',
            name='in_slider',
            field=models.BooleanField(default=True),
        ),
    ]
