from django.urls import include, path
from .views import DetailProduct, CartViewSet, CartItemsViewSet, get_all_products
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register("carts", CartViewSet, basename='carts')
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemsViewSet, basename="cart-items")

urlpatterns = [
    path("products/", get_all_products, name="products"),
    path("products/<int:pk>/", DetailProduct.as_view(), name="singleproduct"),
    path("", include(cart_router.urls)),
    path("carts/", CartViewSet.as_view({'get': 'list'}), name="carts-list"),

]


urlpatterns += router.urls
