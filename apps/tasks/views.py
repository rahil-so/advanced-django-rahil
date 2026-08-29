from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.response import Response
from .permission import TaskPermission
from rest_framework.decorators import action

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated,TaskPermission]
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ['title']
    ordering_fields = ['due_date','priority','created_at']
    ordering = 'priority'

    def get_queryset(self):
        return Task.objects.filter(project__organization__memberships__user=self.request.user)

    @action(methods=['POST'], detail=True)
    def complete(self,request,pk=None):
        task= self.get_object()
        task.is_done= True
        task.save()
        return Response({'message':'Task completed!'})




