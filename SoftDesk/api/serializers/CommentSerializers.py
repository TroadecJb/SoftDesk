from rest_framework import serializers

from api.models.Comment import Comment


class CommentListSerializer(serializers.ModelSerializer):
    """
    Comment serializer as list, without the text content of the comment : description.
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "created_time",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Comment serializer as focus object, with the text content of the comment : description.
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "created_time",
            "description",
        ]
