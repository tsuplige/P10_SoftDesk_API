# Generated by Django 4.2.5 on 2023-10-25 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("softdesk_app", "0003_comment_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="contributor",
            name="role",
            field=models.CharField(choices=[], default="AUTHOR", max_length=100),
            preserve_default=False,
        ),
    ]