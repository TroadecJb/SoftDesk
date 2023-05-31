from django.db import models
from django.conf import settings


class Contributor(models.Model):
    """Contributor model."""

    # Permission Choices
    FULL = "FULL"
    LIMITED = "LIMITED"
    PERMISSION_CHOICES = [
        (FULL, "total"),
        (LIMITED, "partiel"),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="contributors_user",
        on_delete=models.SET_NULL,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="contributors_project",
    )
    permission = models.CharField(
        max_length=20, choices=PERMISSION_CHOICES, default=LIMITED
    )
    role = models.CharField(max_length=30, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "project",
                ],
                name="project_contributor",
            )
        ]

    def __str__(self) -> str:
        return f"User: {self.user}, project: {self.project}"
