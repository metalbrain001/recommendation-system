# Generated by Django 4.2.16 on 2024-10-20 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_tags_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(blank=True, max_length=255)),
                ('tmdb_id', models.CharField(blank=True, max_length=255)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.movie')),
            ],
            options={
                'verbose_name_plural': 'Links',
            },
        ),
    ]