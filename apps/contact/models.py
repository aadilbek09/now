from django.db import models


class Message(models.Model):
    """Sayt kontakt formasi orqali kelgan xabar."""

    name = models.CharField(max_length=150)          # kimdan
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255, blank=True, null=True, help_text="Xabar mavzusi")
    text = models.TextField()
    reply = models.TextField(blank=True, default='', help_text="Admin javobi")
    reply_created_at = models.DateTimeField(blank=True, null=True, help_text="Javob berilgan vaqt")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"


class NewsletterSubscriber(models.Model):
    """Newsletter obunachisi."""

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter obunachisi'
        verbose_name_plural = 'Newsletter obunachilari'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    """Mijozlar sharhi ("Happy Customers")."""

    name = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mijoz sharhi'
        verbose_name_plural = 'Mijozlar sharhlari'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
