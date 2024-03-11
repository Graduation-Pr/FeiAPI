from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemSerializer


router = DefaultRouter()
router.register("", OrderViewSet, basename="orders")
# router.register("items")
urlpatterns = []

urlpatterns += router.urls
