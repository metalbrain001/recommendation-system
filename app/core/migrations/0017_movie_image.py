# Generated by Django 5.1.2 on 2024-11-03 03:50

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_movie_poster_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.user_image_file_path),
        ),
    ]
