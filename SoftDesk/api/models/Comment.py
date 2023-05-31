from django.db import models
from django.conf import settings


class Comment(models.Model):
    """Comment model."""

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
