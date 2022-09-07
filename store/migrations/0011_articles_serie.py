# Generated by Django 4.1 on 2022-08-18 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_series"),
    ]

    operations = [
        migrations.AddField(
            model_name="articles",
            name="serie",
            field=models.ForeignKey(
               # default="None",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to="store.series",
            ),
        ),
    ]
