from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from api.models import Project, Contributor

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
EDIT_METHODS = ("PUT", "PATCH", "POST")
AUHTOR_METHODS = ("DELETE",)


def in_contributors(user, project_id):
    for contributor in Contributor.objects.filter(project=project_id):
        if user == contributor.user:
            return True
    return False


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return in_contributors(
                request.user,
                Project.objects.filter(pk=view.kwars["project_pk"]),
            )
        elif request.method in EDIT_METHODS or AUHTOR_METHODS:
            return (
                request.user
                == Project.objects.filter(pk=view.kwars["project_pk"]).author
            )
        else:
            return False


class ProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return in_contributors(request.user, obj)
        elif request.method in EDIT_METHODS:
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False


class IssuePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or EDIT_METHODS:
            return in_contributors(request.user, view.kwargs["project_pk"])
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return in_contributors(request.user, obj.project)
        elif request.method in EDIT_METHODS:
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.method, "yeha")
        if request.method in EDIT_METHODS or SAFE_METHODS:
            return in_contributors(request.user, view.kwargs["project_pk"])

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return in_contributors(request.user, obj.issue.project)
        elif request.method in EDIT_METHODS:
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False
