from django.urls import path
from .views import get_all_labs, DetailLaboratory


urlpatterns = [
    path("", get_all_labs, name="labs"),
    path("<int:pk>/", DetailLaboratory.as_view(), name="singlelab"),
]
