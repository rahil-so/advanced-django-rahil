from rest_framework import serializers
from .models import Project ,StatusChoices

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
            'id', 'name', 'description', 'organization', 'owner', 'status',
            'status_display', 'deadline','tasks_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id','owner', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'discription': {'required':False, 'allow_null': True},
            'deadline': {'required':False,  'allow_null':True},

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

    





