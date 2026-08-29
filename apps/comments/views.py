from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.filters import OrderingFilter
from .permission import CommentPermission

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,CommentPermission]
    filter_backends = [OrderingFilter]
    ordering_fields = ('created_at',)
    ordering = ('created_at',)

    def get_queryset(self):
        return Comment.objects.filter(task__project__organization__memberships__user=
                                      self.request.user)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)












