from rest_framework import serializers
from .models import BlogPost, BlogImage

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'uploaded_at']

class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)  # Nested serialization

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'likes', 'dislikes', 'created_at', 'images']
