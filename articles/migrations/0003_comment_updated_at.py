# Generated by Django 4.2 on 2024-09-17 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
