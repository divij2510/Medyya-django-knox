# Generated by Django 5.0.3 on 2024-04-19 22:32

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='http://res.cloudinary.com/dk3tpyyee/image/upload/v1713565892/bpwwih53rqle48wt7bsw.png', max_length=255, verbose_name='profile_pictures'),
        ),
    ]