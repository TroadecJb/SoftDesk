from django.db import models
from django.conf import settings


class Issue(models.Model):
    """Issue model."""

    # Priority Choices
    LOW = "LOW"
    MID = "MID"
    HIGH = "HIGH"
    PRIORITY_CHOICES = [
        (LOW, "faible"),
        (MID, "moyenne"),
        (HIGH, "élevée"),
    ]

    # Tag Choices
    BUG = "BUG"
    IMPROVEMENT = "IMPROVEMENT"
    TASK = "TASK"
    TAG_CHOICES = [
        (BUG, "bug"),
        (IMPROVEMENT, "amélioration"),
        (TASK, "tâche"),
    ]

    # Status Choices
    TO_DO = "TO_DO"
    ONGOING = "ONGOING"
    DONE = "DONE"
    STATUS_CHOICES = [
        (TO_DO, "à faire"),
        (ONGOING, "en cours"),
        (DONE, "terminé"),
    ]

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now=True)
    tag = models.CharField(
        max_length=30, choices=TAG_CHOICES, verbose_name="tag"
    )
    priority = models.CharField(
        max_length=30, choices=PRIORITY_CHOICES, verbose_name="priorité"
    )
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, verbose_name="status"
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="issue_author",
        null=True,
    )
    assignee = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="issue",
        null=True,
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="issues"
    )

    def __str__(self):
        return f"issue: {self.id}, {self.title} - project: {self.project}"
