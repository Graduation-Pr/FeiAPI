from django.urls import path
from .views import (
    DetailDevice,
    DetailMedicine,
    get_all_products,
    get_all_devices,
    get_all_medicines,
    cart_detail,
    cart_item_detail,
    add_cart_item,
    get_all_pharmacies
)


urlpatterns = [
    path("", get_all_pharmacies, name="pharmacies"),
    path("products/", get_all_products, name="products"),
    path("devices/", get_all_devices, name="products"),
    path("medicines/", get_all_medicines, name="products"),
    path("devices/<int:pk>/", DetailDevice.as_view(), name="single_device"),
    path("medicines/<int:pk>/", DetailMedicine.as_view(), name="single_medcine"),
    path("carts/", cart_detail),
    path("carts/items/<int:item_pk>/", cart_item_detail),
    path("carts/items/", add_cart_item),
]
