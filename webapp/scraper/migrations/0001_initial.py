# Generated by Django 5.1 on 2024-09-03 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SpecializedBike",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "size",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "bike_class",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "type",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "subtype",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("price", models.FloatField(blank=True, default=None, null=True)),
                ("url", models.URLField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
