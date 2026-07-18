from django.urls import path

from .views import (
    AdminGalleryCreateView,
    AdminGalleryDeleteView,
    AdminRestaurantInfoUpdateView,
    GalleryListView,
    ImageUploadView,
    RestaurantInfoView,
)

urlpatterns = [
    path('upload/image', ImageUploadView.as_view(), name='upload-image'),
    path('gallery/', GalleryListView.as_view(), name='gallery-list'),
    path('restaurant-info/', RestaurantInfoView.as_view(), name='restaurant-info'),
    path('admin/gallery', AdminGalleryCreateView.as_view(), name='admin-gallery-create'),
    path('admin/gallery/<int:pk>', AdminGalleryDeleteView.as_view(), name='admin-gallery-delete'),
    path('admin/restaurant-info/<int:pk>', AdminRestaurantInfoUpdateView.as_view(), name='admin-restaurant-info-update'),
]
