from django.db import models, transaction
from django.conf import settings


class Contributor(models.Model):
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
    role = models.CharField(max_length=30)

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


class Project(models.Model):
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

    # @transaction.atomic
    # def create(self):


class Issue(models.Model):
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


class Comment(models.Model):
    description = models.CharField(max_length=200)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comment_author",
    )
    issue = models.ForeignKey(
        "Issue",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"comment: {self.id} - issue: {self.issue}"
