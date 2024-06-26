"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin site
    path("accounts/", include("accounts.urls")),  # Accounts app URLs
    path("pharmacy/", include("pharmacy.urls")),  # Pharmacy app URLs
    path("patients/", include("patient.urls")),  # Patient app URLs
    path("labs/", include("laboratory.urls")),  # Laboratory app URLs
    path("orders/", include("orders.urls")),  # Orders app URLs
    path("doctors/", include("doctor.urls")),  # Doctors app URLs

    # API schema and documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),  # Swagger UI
    path("swagger/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),  # Redoc UI
]

# Serve static and media files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
