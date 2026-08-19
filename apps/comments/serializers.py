from rest_framework.serializers import Serializer ,ModelSerializer
from apps.comments.models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = [
            'author',
            'created_at'
            'updated_at',
        ]

class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = [
            'author',
            'created_at',
            'updated_at',
        ]
