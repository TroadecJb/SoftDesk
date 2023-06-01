from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


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
    """
    Returns a list of projects where the user is a contributor.
    """
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
    """Viewset for actions on a project object."""

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, permissions.ProjectPermission]

    def get_queryset(self):
        """
        Get the projects list of the request user.
        Or get the project's detail if the project's id is specified in the reques.
        """
        if self.detail is True:
            project_id = self.kwargs["pk"]
            if project_exists(project_id):
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
    """Viewset for actions on project's contributors."""

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, permissions.ContributorPermission]

    def get_queryset(self):
        """Get the project's contributors list."""
        project_id = self.kwargs["project_pk"]
        if project_exists(project_id):
            project = Project.objects.get(id=project_id)
            return self.queryset.filter(project=project)

    def perform_create(self, serializer):
        """Add a user as contributor to the project."""
        project_id = self.kwargs["project_pk"]
        if project_exists(project_id):
            project = Project.objects.get(id=project_id)
            serializer.save(project=project)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    """Viewwset for actions on project's issues."""

    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, permissions.IssuePermission]

    def get_queryset(self):
        """Get the issue(s) for the project."""
        project_id = self.kwargs["project_pk"]
        if project_exists(project_id):
            return Issue.objects.filter(project__in=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        """
        Create a new issue for the project if it exists.
        The issue's assignee can be specify otherwise the request user is set by default as the assignee.
        """
        project_id = self.kwargs["project_pk"]
        if project_exists(project_id):
            project = Project.objects.get(id=project_id)
            if not self.request.data["assignee"]:
                serializer.save(
                    author=self.request.user,
                    assignee=self.request.user,
                    project=project,
                )
            else:
                serializer.save(author=self.request.user, project=project)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    """Viewset for actions on issue's comments."""

    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, permissions.CommentPermission]

    def get_queryset(self):
        """Get the comment(s) for the issue."""
        issue_id = self.kwargs["issues_pk"]
        if issue_exists(issue_id):
            return self.queryset.filter(issue__in=self.kwargs["issues_pk"])

    def perform_create(self, serializer):
        """
        Create a new comment for the issue if it exists.
        """
        issue_id = self.kwargs["issues_pk"]
        if issue_exists(issue_id):
            issue = Issue.objects.get(id=issue_id)
            serializer.save(author=self.request.user, issue=issue)
