# Generated by Django 4.1 on 2022-08-13 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_remove_thepictures_id_thepictures_rank_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="articles", name="id",),
        migrations.AlterField(
            model_name="articles",
            name="name",
            field=models.CharField(
                max_length=100, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
