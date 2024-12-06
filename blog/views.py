from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import BlogPost
from .serializers import BlogPostSerializer

# List all posts
class PostListView(APIView):
    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')  # Order by latest
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

# Retrieve a single post
class PostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

# Create a new post
class PostCreateView(APIView):
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            blog_post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Debugging step to view validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
