# Generated by Django 4.1 on 2022-08-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0018_alter_articles_fileprincipal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articles",
            name="filePrincipal",
            field=models.CharField(default="", max_length=3000),
        ),
    ]
