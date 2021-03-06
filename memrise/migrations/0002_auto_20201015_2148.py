# Generated by Django 3.1.2 on 2020-10-15 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("memrise", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="level",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="levels",
                to="memrise.course",
            ),
        ),
        migrations.AlterField(
            model_name="word",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="words",
                to="memrise.level",
            ),
        ),
        migrations.AlterField(
            model_name="word",
            name="word_a",
            field=models.CharField(
                default="", max_length=1024, verbose_name="Original word"
            ),
        ),
        migrations.AlterField(
            model_name="word",
            name="word_b",
            field=models.CharField(
                default="", max_length=1024, verbose_name="Translate"
            ),
        ),
    ]
