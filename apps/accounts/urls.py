from django.urls import path

from .views import (
    AdminLoginView,
    ChangePasswordView,
    LoginView,
    LogoutView,
    MeUpdateView,
    MeView,
    PublicProfileView,
    RefreshView,
    RegisterView,
)

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('auth/refresh', RefreshView.as_view(), name='auth-refresh'),
    path('auth/logout', LogoutView.as_view(), name='auth-logout'),
    path('auth/me', MeView.as_view(), name='auth-me'),
    path('auth/me/update', MeUpdateView.as_view(), name='auth-me-update'),
    path('auth/change-password', ChangePasswordView.as_view(), name='auth-change-password'),
    path('profile/<slug:username>', PublicProfileView.as_view(), name='public-profile'),
    path('admin/auth/login', AdminLoginView.as_view(), name='admin-auth-login'),
]
