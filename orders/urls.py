from .views import OrderViewSet, list_credit_card, credit_card_detail, credit_card_create
from rest_framework.routers import DefaultRouter
from django.urls import path

# Initialize the DefaultRouter
router = DefaultRouter()
# Register the OrderViewSet with the router
router.register("", OrderViewSet, basename="orders")
# Define urlpatterns for the Credit Card related views
urlpatterns = [
    # Endpoint to list all credit cards for the authenticated user and create new credit card
    path('credit_cards/', list_credit_card, name='credit_card_list'),
    path('credit_cards/create/', credit_card_create, name='credit_card_create'),
    # Endpoint to retrieve or delete a specific credit card
    path('credit_cards/<int:pk>/', credit_card_detail, name='credit_card_detail'),
]
# Add the router's URLs to the urlpatterns
urlpatterns+=router.urls