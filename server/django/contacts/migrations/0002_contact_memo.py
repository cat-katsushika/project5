# Generated by Django 5.0.4 on 2024-04-07 22:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="memo",
            field=models.TextField(blank=True),
        ),
    ]
