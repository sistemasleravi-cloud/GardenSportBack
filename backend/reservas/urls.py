from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CanchaViewSet, ReservaViewSet, UserViewSet

router = DefaultRouter()
router.register(r'canchas', CanchaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]