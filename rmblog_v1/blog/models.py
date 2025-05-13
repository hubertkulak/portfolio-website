from django.db import models

# Create your models here.
class NewPost(models.Model):
    title = models.CharField(max_length=200)
    slug=models.SlugField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#Can be used instead of content inside html template
    def content_shortcut(self):
        return self.content[:100]