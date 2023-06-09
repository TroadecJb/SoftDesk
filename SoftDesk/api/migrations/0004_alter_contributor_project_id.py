# Generated by Django 4.2.1 on 2023-05-24 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_alter_comment_author_user_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="project_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributors_project",
                to="api.project",
            ),
        ),
    ]
