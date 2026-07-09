from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from apps.article.models import Article
from apps.article.serializers import ArticleSerializer, ArticleDetailSerializer, ArticleCSVSerializer
from rest_framework import generics
from apps.article.permissions import ArticleOwnerPermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.core.cache import cache
from django.views.decorators.cache import  cache_page
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from apps.article.tasks import import_article_from_csv_task
from apps.users.models import User
from celery.result import AsyncResult

class ArticleListAPIView(APIView):
    permission_classes = [AllowAny]

    @cache_page(60 * 5)
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        cache_key = f'article:{pk}-{request.user.id}'
        article = cache.get(cache_key)
        if not article:
            article = get_object_or_404(Article, pk=pk)
            cache.set(cache_key, article, timeout=5 * 60)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(pk)
        cache.set(pk, article, timeout=5 * 60)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(pk)
        cache.set(pk, article, timeout=5 * 60)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        cache.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)



class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    pagination_class = None
    def get_queryset(self):

        return Article.objects.all()
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, ArticleOwnerPermission]

    # def get_serializer_class(self):
    #     if request.method in( 'GET', 'PUT', 'PATCH'):
    #         return ArticleDetailSerializer
    #     else:
    #         return ArticleSerializer
    #
    # def perform_update(self, serializer):
    #     serializer.save(author=self.request.user)
    #
    # def perform_destroy(self, serializer):
    #     serializer.save(author=self.request.user)


@method_decorator(cache_page(60 * 5), name='dispatch')
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.is_published = True
        article.save()
        add.delay(8,9)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='published-articles')
    def published_articles(self, request):
        articles = Article.objects.filter(is_published=True)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AddArticleFromCSV(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
       file = request.FILES['file']
       task = import_article_from_csv_task.delay(file.read().decode())
       return Response(data={'task_id': task.id}, status=status.HTTP_201_CREATED)


class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, task_id):
        task = AsyncResult(task_id=task_id)
        return Response({'status': task.status, 'result': task.result}, status=status.HTTP_200_OK)


