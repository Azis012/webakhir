# Generated by Django 5.0.6 on 2024-06-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UploadFiles", "0006_myfileupload_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="myfileupload",
            name="selected",
            field=models.BooleanField(default=False),
        ),
    ]
