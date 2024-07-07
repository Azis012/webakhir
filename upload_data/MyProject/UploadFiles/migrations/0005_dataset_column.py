# Generated by Django 5.0.6 on 2024-06-21 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UploadFiles", "0004_myfileupload_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("status", models.CharField(default="", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Column",
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
                ("name", models.CharField(max_length=255)),
                ("data_type", models.CharField(max_length=255)),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="columns",
                        to="UploadFiles.dataset",
                    ),
                ),
            ],
        ),
    ]
