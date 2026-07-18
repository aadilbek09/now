from django.urls import path

from .views import (
    AdminGalleryCreateView,
    AdminGalleryDeleteView,
    AdminRestaurantInfoUpdateView,
    GalleryListView,
    ImageUploadView,
    RestaurantInfoView,
    serve_frontend,
)

urlpatterns = [
    path('upload/image', ImageUploadView.as_view(), name='upload-image'),
    path('gallery/', GalleryListView.as_view(), name='gallery-list'),
    path('restaurant-info/', RestaurantInfoView.as_view(), name='restaurant-info'),
    path('admin/gallery', AdminGalleryCreateView.as_view(), name='admin-gallery-create'),
    path('admin/gallery/<int:pk>', AdminGalleryDeleteView.as_view(), name='admin-gallery-delete'),
    path('admin/restaurant-info/<int:pk>', AdminRestaurantInfoUpdateView.as_view(), name='admin-restaurant-info-update'),

    # ---------- Frontend (Static HTML) ----------
    path('', serve_frontend, {'page': 'index.html'}, name='home'),
    path('menu/', serve_frontend, {'page': 'menu.html'}, name='menu'),
    path('news/', serve_frontend, {'page': 'news.html'}, name='news'),
    path('about/', serve_frontend, {'page': 'about.html'}, name='about'),
    path('contact/', serve_frontend, {'page': 'contact.html'}, name='contact'),
    path('login/', serve_frontend, {'page': 'login.html'}, name='login'),
    path('register/', serve_frontend, {'page': 'register.html'}, name='register'),
    path('profile/', serve_frontend, {'page': 'profile.html'}, name='profile'),
    path('admin-panel/', serve_frontend, {'page': 'admin-panel.html'}, name='admin-panel'),
    path('product/<int:pk>/', serve_frontend, {'page': 'product-detail.html'}, name='product-detail'),
]
