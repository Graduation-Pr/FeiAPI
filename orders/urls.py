from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, list_credit_card, credit_card_detail, credit_card_create



router = DefaultRouter()
router.register("", OrderViewSet, basename="orders")
# router.register("items")
urlpatterns = [
    path('credit_cards/', list_credit_card, name='credit_card_list'),
    path('credit_cards/create/', credit_card_create, name='credit_card_create'),
    path('credit_cards/<int:pk>/', credit_card_detail, name='credit_card_detail'),
]

urlpatterns += router.urls

