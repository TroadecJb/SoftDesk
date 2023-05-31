from rest_framework import serializers
from api.models.Project import Project
from api.serializers.IssueSerializers import IssueListSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Project serializer as list, without the isssues related objects.
    """

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
    """
    Project serializer as focus object, with the issues related objects (as list).
    """

    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "issues",
        ]

    def get_issues(self, instance):
        queryset = instance.issues
        return IssueListSerializer(queryset, many=True).data
