# Generated by Django 3.1.2 on 2020-11-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memrise', '0003_course_is_disable'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='is_learned',
            field=models.BooleanField(default=False, verbose_name='Learn state'),
        ),
    ]