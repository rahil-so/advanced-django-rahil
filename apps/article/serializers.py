from django.core.validators import FileExtensionValidator
from rest_framework.serializers import Serializer, ModelSerializer
from apps.article.models import Article, Tag
from apps.users.models import User
from rest_framework import serializers
class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class MiniAuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ArticleSerializer(ModelSerializer):
    author = MiniAuthorSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'author', 'tags', 'created_at', 'updated_at', 'is_published')
        read_only_fields = ('id','created_at', 'updated_at')

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        return value

    def validate(self, attrs):
        if attrs.get('title') and attrs.get('body'):
            if not attrs.get('title') in attrs.get('body'):
                raise serializers.ValidationError("Title must be inside body")
        return attrs

    def create(self, validated_data):
        tags_data = validated_data.pop('tags',None)
        new_article = Article.objects.create(**validated_data)
        tags_d = []
        for tag in tags_data:

            t,_ = Tag.objects.get_or_create(name=tag['name'])
            tags_d.append(t)
        new_article.tags.add(*tags_d)
        new_article.save()
        return new_article



    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.author = instance.author
        if tags_data:
            instance.tags.clear()
            for tag in tags_data:
                tag,_ = Tag.objects.get_or_create(**tag)
                instance.tags.add(tag)
        return instance




class ArticleDetailSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Article

