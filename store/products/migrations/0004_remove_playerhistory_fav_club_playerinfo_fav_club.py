# Generated by Django 5.1.4 on 2025-01-16 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_playerhistory"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playerhistory",
            name="fav_club",
        ),
        migrations.AddField(
            model_name="playerinfo",
            name="fav_club",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="products.playerhistory",
            ),
        ),
    ]
