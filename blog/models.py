from django.db import models
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")  # HTML content generated dynamically
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)  # Track post views
    slug = models.SlugField(unique=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, default="")  # Tags for the blog post
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Custom ordering by creation date, newest first

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.blog_post.title}"