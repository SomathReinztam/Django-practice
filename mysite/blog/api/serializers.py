from rest_framework import serializers
from ..models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "slug", "author", "body", "status"]


class PostAuthorSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Post
        fields = ["author"]


class AuthorPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "status"]
