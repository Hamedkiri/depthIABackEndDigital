# Generated by Django 4.1 on 2022-08-13 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_remove_articles_id_alter_articles_name"),
    ]

    operations = [
        migrations.DeleteModel(name="ThePictures",),
    ]