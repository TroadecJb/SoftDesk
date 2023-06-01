from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from api.models import Project
from api.check import user_is_contributor

SAFE_METHODS = (
    "GET",
    "HEAD",
    "OPTIONS",
)
AUHTOR_METHODS = ("PUT", "PATCH")


class ContributorPermission(BasePermission):
    """
    Contributors can RETRIEVE and LIST.
    Author can EDIT, PARTIAL EDIT, POST and DELETE.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return user_is_contributor(
                request.user.id, view.kwargs["project_pk"]
            )
        elif request.method in AUHTOR_METHODS or "POST" or "DELETE":
            return (
                request.user
                == Project.objects.get(pk=view.kwargs["project_pk"]).author
            )
        else:
            return False


class ProjectPermission(BasePermission):
    """
    Any authenticated user can CREATE.
    Contributors can GET.
    Author, admin and superuser can DELETE.
    Author can EDIT and PARTIAL EDIT.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return user_is_contributor(request.user.id, obj.id)
        elif request.method == "DELETE":
            return (
                request.user.is_admin
                or request.user == obj.author
                or request.user.is_superuser
            )
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author
        else:
            return False


class IssuePermission(BasePermission):
    """
    Contributors can GET and POST.
    Author, admin and superuser can DELETE.
    Author can EDIT and PARTIAL EDIT.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or "POST":
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
            return (
                request.user.is_admin
                or request.user == obj.author
                or request.user.is_superuser
            )
        elif request.method in AUHTOR_METHODS:
            return request.user == obj.author
        else:
            return False


class CommentPermission(BasePermission):
    """
    Contributors can GET and POST.
    Author, admin and superuser can DELETE.
    Author can EDIT and PARTIAL EDIT.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or "POST":
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
            return request.user == obj.author
        else:
            return False
