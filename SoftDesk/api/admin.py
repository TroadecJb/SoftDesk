from django.contrib import admin
from api.models import Contributor, Project, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
    ]


class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "project",
        "author",
        "assignee",
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "issue",
        "author",
    ]


class ContributorAdmin(admin.ModelAdmin):
    list_display = ["user", "user_id", "project"]


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
