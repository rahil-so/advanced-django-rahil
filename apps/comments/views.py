from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.filters import OrderingFilter

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ('created_at',)
    ordering = ('created_at',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)







