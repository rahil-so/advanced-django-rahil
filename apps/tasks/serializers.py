from rest_framework.serializers import Serializer,ModelSerializer,PrimaryKeyRelatedField
from apps.tasks.models import Task
from apps.users.models import User
from apps.users.serializers import UserBriefSerializer
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    assignee_detail =UserBriefSerializer(source='assignee', read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        allow_null=True,

    )
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'assignee', 'assignee_detail', 'reporter', 'priority',
            'priority_label', 'is_done', 'due_date', 'estimated_hours', 'tags', 'comments_count', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'reporter', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        request = self.context['request']
        validated_data['reporter'] = request.user
        return super().create(validated_data)
