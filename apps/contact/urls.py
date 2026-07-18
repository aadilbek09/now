from django.urls import path

from .views import (
    AdminMessageDeleteView,
    AdminMessageListView,
    AdminMessageMarkReadView,
    AdminNewsletterSubscriberListView,
    AdminTestimonialCreateView,
    AdminTestimonialDeleteView,
    AdminTestimonialUpdateView,
    ContactMessageCreateView,
    NewsletterSubscribeView,
    TestimonialListView,
)

urlpatterns = [
    path('contact', ContactMessageCreateView.as_view(), name='contact-create'),
    path('admin/messages', AdminMessageListView.as_view(), name='admin-message-list'),
    path('admin/messages/<int:id>/read', AdminMessageMarkReadView.as_view(), name='admin-message-read'),
    path('admin/messages/<int:id>', AdminMessageDeleteView.as_view(), name='admin-message-delete'),
    path('admin/testimonials', AdminTestimonialCreateView.as_view(), name='admin-testimonial-create'),
    path('admin/testimonials/<int:pk>', AdminTestimonialUpdateView.as_view(), name='admin-testimonial-update'),
    path('admin/testimonials/<int:pk>/delete', AdminTestimonialDeleteView.as_view(), name='admin-testimonial-delete'),
    path('admin/newsletter/subscribers', AdminNewsletterSubscriberListView.as_view(), name='admin-newsletter-subscribers'),
    path('newsletter/subscribe', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('testimonials', TestimonialListView.as_view(), name='testimonial-list'),
]
