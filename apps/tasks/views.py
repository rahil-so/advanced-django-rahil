from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from models import Task
from serializers import TaskSerializer
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.response import Response

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_class = [IsAuthenticated]
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ['title']
    ordering_fields = ['duo_date','priority','created_at']
    ordering = 'priority'

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

    def perform_update(self, serializer):
        serializer.save(assignee=self.request.user)

    def get_permissions(self):
        if self.action in  ['list','retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def complete(self,request,pk=None):
        task= self.get_object()
        task.set_status= 'completed'
        task.save()
        return Response({'message':'Task completed!'})

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return TaskSerializer
    #     if self.action == 'list':
    #         return TaskSerializer
    #     if self.action == 'create':
    #         return TaskSerializer


