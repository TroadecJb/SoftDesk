from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from api.models import Project, Contributor, Issue, Comment
from api.check import user_is_contributor

SAFE_METHODS = ("GET", "HEAD", "OPTIONS", "POST")
AUHTOR_METHODS = ("PUT", "PATCH")


class ContributorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )
        elif request.method in AUHTOR_METHODS or "DELETE":
            return (
                request.user
                == Project.objects.filter(pk=view.kwars["project_pk"]).author
            )
        else:
            return False


class ProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return user_is_contributor(request.user.id, obj.id)
        elif request.method == "DELETE":
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS or "DELETE":
            return request.user == obj.author or request.user.is_superuser
        else:
            return False


class IssuePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )
        elif request.method == "DELETE":
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )
        elif request.method in "DELETE":
            return request.user.is_admin or request.user == obj.author
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author or request.user.is_superuser
        else:
            return False
