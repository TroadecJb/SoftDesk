from rest_framework import serializers

from api.models import Project, Issue, Comment, Contributor
from account.models import CustomUser
from account.serializers import CustomUserSerializer


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            # "project",
            "permission",
            "role",
        ]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            # "issue",
            "author",
            "created_time",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            # "issue",
            "author",
            "created_time",
            "description",
        ]


class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "description",
            "created_time",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "description",
            "created_time",
            "comments",
        ]

    def get_comments(self, instance):
        queryset = instance.comments
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(serializers.ModelSerializer):
    author_user_id = serializers

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            # "contributors",
            "issues",
        ]

    def get_issues(self, instance):
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data
