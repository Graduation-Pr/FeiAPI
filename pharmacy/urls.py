from django.urls import include, path
from .views import ListProduct, DetailProduct, CartViewSet, CartItemsViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register("carts", CartViewSet)
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemsViewSet, basename="cart-items")

urlpatterns = [
    path("products/", ListProduct.as_view(), name="products"),
    path("products/<int:pk>/", DetailProduct.as_view(), name="singleproduct"),
    path("", include(cart_router.urls)),
]


urlpatterns += router.urls
