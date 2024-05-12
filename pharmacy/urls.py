from django.urls import include, path
from .views import (
    DetailDevice,
    DetailMedicine,
    CartViewSet,
    CartItemsViewSet,
    get_all_products,
    get_all_devices,
    get_all_medicines,
    
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register("carts", CartViewSet, basename="carts")
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemsViewSet, basename="cart-items")

urlpatterns = [
    path("products/", get_all_products, name="products"),
    path("devices/", get_all_devices, name="products"),
    path("medicines/", get_all_medicines, name="products"),
    path("devices/<int:pk>/", DetailDevice.as_view(), name="single_device"),
    path("medicines/<int:pk>/", DetailMedicine.as_view(), name="single_medcine"),
    path("", include(cart_router.urls)),
    path("carts/", CartViewSet.as_view({"get": "list"}), name="carts-list"),
]


urlpatterns += router.urls
