# Generated by Django 5.1.4 on 2025-01-26 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_playerhistory_playerinfo_fav_club"),
    ]

    operations = [
        migrations.CreateModel(
            name="patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("age", models.IntegerField()),
                ("address", models.CharField(max_length=250)),
                ("disease_pic", models.ImageField(upload_to="images/")),
            ],
        ),
    ]
