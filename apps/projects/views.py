from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.filters import OrderingFilter,SearchFilter


class ProjectViewSet(ModelViewSet):
    lookup_field = 'slug'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [OrderingFilter,SearchFilter]
    search_fields = ['name']
    ordering_fields = ['deadline','status','created_at']
    ordering = 'deadline'


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return  Project.objects.filter(owner=self.request.user)


    def get_permissions(self):
        if self.action == 'list':
            permission_classes =[IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

