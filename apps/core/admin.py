from django.contrib import admin

from .models import GalleryImage, RestaurantInfo


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'created_at')


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'phone', 'working_hours', 'updated_at')
