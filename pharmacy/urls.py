from django.urls import path
from .views import ListCategory, DetailCategory, ListProduct, DetailProduct
urlpatterns = [
    path('categories/', ListCategory.as_view(), name='categorie'),
    path('categories/<int:pk>/', DetailCategory.as_view(), name='singlecategory'),
    
    path('products/', ListProduct.as_view(), name='products'),
    path('products/<int:pk>/', DetailProduct.as_view(), name='singleproduct'),

]
