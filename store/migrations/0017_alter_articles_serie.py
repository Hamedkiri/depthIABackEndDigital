# Generated by Django 4.1 on 2022-08-18 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0016_series_articles_serie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articles",
            name="serie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to="store.series",
            ),
        ),
    ]
