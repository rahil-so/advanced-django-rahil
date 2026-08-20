from rest_framework import serializers
from apps.users.serializers import UserBriefSerializer, User
from .models import Project ,StatusChoices
from apps.tasks.models import Task

class ProjectStatSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(read_only=True)
    project_name = serializers.CharField(read_only=True)
    total_tasks = serializers.IntegerField(read_only=True)
    completed_tasks = serializers.IntegerField(read_only=True)
    completed_percentage = serializers.FloatField(read_only=True)
    overdue_tasks = serializers.IntegerField(read_only=True)
    members_count = serializers.IntegerField(read_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'organization', 'owner', 'status', 'status_display', 'deadline','task_count', 'created_at', 'updated_at'
        ]

        read_only_fields = [
            'id','owner', 'created_at', 'updated_at'
        ]

        extra_kwargs = {
            'discription': {'required':False, 'allow_null': True},
            'deadline': {'required':False,  'allow_null':True},
            'organization': {'write_only':True}

        }

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('این فیلد نمی تواند کمتر از ۳ کاراکتر باشد')
        return value.strip()


    def validate(self, attrs):
        if attrs.get('status') == StatusChoices.COMPLETED and not attrs.get('deadline'):
            raise serializers.ValidationError('پروژه ای که انجام شده باید موعد تحویل داشته باشد')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    


class TaskSerializer(serializers.ModelSerializer):
    assignee_detail = UserBriefSerializer(source='assignee', read_only=True)
    asignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        required=False,
        allow_null=True,

    )
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        models = Task
        fields = [
            'id', 'title', 'description', 'project', 'assignee','assignee_detail', 'reporter','priority','priority_label','is_done','due_date','estimated_hours','tags','comments_count','created_at','updated_at'
        ]
        read_only_fields = [
            'id','reporter','created_at','updated_at'
        ]
        


    def create(self, validated_data):
        request = self.context['request']
        validated_data['reporter'] = request.user
        return super().create(validated_data)



