from django.urls import path
from .views import get_all_docs, DoctorDetail

urlpatterns = [
    path("", get_all_docs, name="doctor-list"),
    path("<int:pk>/", DoctorDetail.as_view(), name="doctor"),
]
