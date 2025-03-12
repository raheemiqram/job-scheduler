# Generated by Django 5.0.8 on 2025-03-11 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job", "0002_job_wait_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="priority",
            field=models.IntegerField(choices=[(1, "High"), (2, "Medium"), (3, "Low")]),
        ),
    ]
