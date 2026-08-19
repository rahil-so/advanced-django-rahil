from rest_framework.serializers import Serializer,ModelSerializer
from tasks.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id',
                  'created_at',
                  'updated_at',
                  'title',
                  'description',
                  'project',
                  'assignee',
                  'reporter',
                  'priority',
                  'is_done',
                  'due_date',
                  'estimated_hours',
                  'tags'

                  ]
        read_only_fields = [
            'reporter',
            'id'
            'created_at',
            'updated_at',
        ]
