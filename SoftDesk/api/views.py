from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from api.models import Project, Issue, Comment, Contributor
from api.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    ContributorSerializer,
)
from api import permissions
from api.check import (
    project_exists,
    issue_exists,
    comment_exists,
    contributor_exists,
    user_exists,
)


def list_project_where_contributor(request):
    current_user = request.user.id
    return [
        contributor.project.id
        for contributor in Contributor.objects.filter(user=current_user)
    ]


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.ProjectPermission]

    def get_queryset(self):
        if self.detail is True:
            return Project.objects.filter(id=self.kwargs["pk"])
        else:
            project_list = list_project_where_contributor(self.request)
            return Project.objects.filter(id__in=project_list)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        author_contributor = Contributor(
            user=self.request.user,
            project=serializer.instance,
            permission="total",
            role="auteur",
        )
        author_contributor.save()


class ContributorViewset(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.ContributorPermission]

    def get_queryset(self):
        try:
            project = Project.objects.get(id=self.kwargs["project_pk"])
        except Project.DoesNotExist:
            raise NotFound
        return self.queryset.filter(project=project)

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs["project_pk"])
        serializer.save(project=project)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [permissions.IssuePermission]

    def get_queryset(self):
        return Issue.objects.filter(project__in=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        try:
            project = Project.objects.get(id=self.kwargs["project_pk"])
        except Project.DoesNotExist:
            raise NotFound
        if not self.request.data["assignee"]:
            serializer.save(
                author=self.request.user,
                assignee=self.request.user,
                project=project,
            )
        else:
            serializer.save(author=self.request.user, project=project)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [permissions.CommentPermission]

    def get_queryset(self):
        return self.queryset.filter(issue__in=self.kwargs["issues_pk"])

    def perform_create(self, serializer):
        try:
            issue = Issue.objects.get(id=self.kwargs["issues_pk"])
        except Issue.DoesNotExist:
            raise NotFound
        print(self.kwargs["issues_pk"])
        serializer.save(author=self.request.user, issue=issue)
