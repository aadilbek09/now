from django.db import models


class Post(models.Model):
    """Yangilik / e'lon (News / Announcement)."""

    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True, help_text="Qisqa tavsif / description")
    category = models.CharField(max_length=100, blank=True, null=True, help_text="Post kategoriyasi")
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Postlar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
