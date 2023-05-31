from rest_framework import serializers
from api.models.Issue import Issue
from api.serializers.CommentSerializers import CommentListSerializer


class IssueListSerializer(serializers.ModelSerializer):
    """
    Issue serializer as list, without the comments related objects.
    """

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
    """
    Issue serializer as focus object, with the comments related objects (as list).
    """

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
