# Generated by Django 4.1.3 on 2023-01-23 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_activity_featured_image_strength_featured_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='default',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='gallery',
            name='default',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='default',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
