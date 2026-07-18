from django.contrib import admin

from .models import Message, NewsletterSubscriber, Testimonial


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'phone', 'text')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'subscribed_at')
    search_fields = ('email',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'created_at')
    search_fields = ('name', 'text')
