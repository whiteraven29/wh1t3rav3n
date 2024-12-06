from rest_framework import serializers
from .models import BlogPost, BlogImage

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'uploaded_at']

class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)
    text_blocks = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )
    image_blocks = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )

    class Meta:
        model = BlogPost
        fields = [
            'id', 
            'title', 
            'text_blocks', 
            'image_blocks', 
            'content', 
            'likes', 
            'dislikes', 
            'created_at', 
            'images'
        ]

    def create(self, validated_data):
        text_blocks = validated_data.pop('text_blocks', [])
        image_blocks = validated_data.pop('image_blocks', [])

        # Create the BlogPost
        blog_post = BlogPost.objects.create(**validated_data)

        # Save associated images
        for image in image_blocks:
            BlogImage.objects.create(blog_post=blog_post, image=image)

        # Combine content blocks into the HTML content field
        combined_content = ""
        for text in text_blocks:
            combined_content += f"<p>{text}</p>"
        combined_content += "".join(
            f"<img src='{img.image.url}' alt='Image'>" for img in blog_post.images.all()
        )
        blog_post.content = combined_content
        blog_post.save()

        return blog_post
