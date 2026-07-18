from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Faqat role='admin' bo'lgan, autentifikatsiyadan o'tgan foydalanuvchilarga
    ruxsat beradi. Barcha /api/admin/... endpointlarida ishlatiladi
    (1-a'zo vazifasi: "Admin endpointlarga faqat role=admin kira olishini
    ta'minlash").
    """

    message = "Bu amal uchun admin huquqi talab qilinadi."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'role', None) == 'admin'
        )


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    O'qish (GET, HEAD, OPTIONS) hamma uchun ochiq.
    Yozish (POST, PUT, PATCH, DELETE) uchun autentifikatsiya talab qilinadi.
    """

    message = "Tahrirlash uchun tizimga kirish kerak."

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return bool(request.user and request.user.is_authenticated)