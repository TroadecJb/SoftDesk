# Generated by Django 4.2.1 on 2023-05-25 12:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_remove_contributor_project_contributors_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="contributor",
            name="project_contributors",
        ),
    ]
