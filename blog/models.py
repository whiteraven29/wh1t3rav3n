from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # Supports rich text (HTML format)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog_images/")  # Adjust media folder as needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.blog_post.title}"
