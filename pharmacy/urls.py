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
    get_all_pharmacies,
    add_fav_product,
    list_fav_produts,
)

# Define the URL patterns for the application
urlpatterns = [
    # Endpoint to get all pharmacies
    path("", get_all_pharmacies, name="pharmacies_list"),

    # Endpoints to get all products, devices, and medicines for a specific pharmacy
    path("<int:pk>/products/", get_all_products, name="pharmacy_products"),
    path("<int:pk>/devices/", get_all_devices, name="pharmacy_devices"),
    path("<int:pk>/medicines/", get_all_medicines, name="pharmacy_medicines"),

    # Endpoints to get detailed information about a specific device or medicine
    path("<int:pk>/devices/", DetailDevice.as_view(), name="device_detail"),
    path("medicines/<int:pk>/", DetailMedicine.as_view(), name="medicine_detail"),

    # Endpoint to get the current user's cart details
    path("carts/", cart_detail, name="cart_detail"),

    # Endpoints to get, update, or delete a specific item in the current user's cart
    path("carts/items/<int:item_pk>/", cart_item_detail, name="cart_item_detail"),

    # Endpoint to add an item to the current user's cart
    path("carts/items/", add_cart_item, name="add_cart_item"),

    # Endpoint to add a product to the current user's list of favorite products
    path("products/fav/<int:pk>/", add_fav_product, name="add_fav_product"),

    # Endpoint to get the current user's list of favorite products
    path("products/fav/", list_fav_produts, name="list_fav_products"),
]

