# Generated by Django 4.2.16 on 2024-10-20 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_tags_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]