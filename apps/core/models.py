from django.db import models


class GalleryImage(models.Model):
    """Instagram Gallery fotolari."""

    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gallery fotosi'
        verbose_name_plural = 'Gallery fotolari'
        ordering = ['-created_at']

    def __str__(self):
        return self.caption or f"Foto #{self.id}"


class RestaurantInfo(models.Model):
    """
    Restoran haqqinda uliwma maǵliwmat: mánzili, telefon nomeri, jumis waqiti hám karta. Ádette tek bir jazba boladi (singleton siyaqli qollaniladi).
    """

    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    working_hours = models.CharField(max_length=100, help_text="Masalan: 09:00 - 23:00")
    map_url = models.URLField(blank=True, help_text="Google Maps embed/link URL")
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Restoran ma\u02bbglumati'
        verbose_name_plural = 'Restoran ma\u02bbgliwmatleri'

    def __str__(self):
        return f"Restoran mag'liwmati ({self.address})"
