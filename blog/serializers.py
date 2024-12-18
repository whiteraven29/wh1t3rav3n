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
    content_blocks = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 
            'title', 
            'slug',
            'tags',
            'text_blocks', 
            'image_blocks', 
            'content', 
            'likes', 
            'dislikes', 
            'views',
            'created_at', 
            'images', 
            'content_blocks'
        ]

    def get_content_blocks(self, obj):
        # Combine text and image blocks in the correct order
        content_blocks = []

        # Assuming content is already stored in the `text_blocks` format
        text_blocks = obj.content.split("<p>")[1:] if obj.content else []
        text_blocks = [block.split("</p>")[0] for block in text_blocks]

        for index, text in enumerate(text_blocks):
            content_blocks.append({"type": "text", "value": text})
            # Add corresponding image if available
            if index < obj.images.count():
                content_blocks.append({
                    "type": "image", 
                    "value": obj.images.all()[index].image.url
                })

        # Add remaining images (if text count is less than image count)
        if obj.images.count() > len(text_blocks):
            for img in obj.images.all()[len(text_blocks):]:
                content_blocks.append({"type": "image", "value": img.image.url})

        return content_blocks

    def create(self, validated_data):
        text_blocks = validated_data.pop('text_blocks', [])
        image_blocks = validated_data.pop('image_blocks', [])

        # Create the BlogPost
        blog_post = BlogPost.objects.create(**validated_data)

        # Save associated images
        for image in image_blocks:
            BlogImage.objects.create(blog_post=blog_post, image=image)

        # Combine text blocks for simple HTML content (optional field)
        combined_content = "".join(f"<p>{text}</p>" for text in text_blocks)
        combined_content += "".join(
            f"<img src='{img.image.url}' alt='Image'>" for img in blog_post.images.all()
        )
        blog_post.content = combined_content
        blog_post.save()

        return blog_post
