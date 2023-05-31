from django.db import models
from django.conf import settings


class Project(models.Model):
    """Project model."""

    # Type Choices
    WEB = "WEB"
    ANDROID = "ANDROID"
    IOS = "IOS"
    TYPE_CHOICES = [
        (WEB, "web"),
        (ANDROID, "android"),
        (IOS, "ios"),
    ]

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    type = models.CharField(
        max_length=40, choices=TYPE_CHOICES, verbose_name="type"
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.id}, {self.title}"
