# Generated by Django 5.0.6 on 2024-06-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UploadFiles", "0002_myfileupload_creator_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myfileupload",
            name="my_file",
            field=models.FileField(upload_to="csv/"),
        ),
    ]
