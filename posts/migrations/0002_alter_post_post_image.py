# Generated by Django 5.0.3 on 2024-04-19 21:56

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='post_images'),
        ),
    ]