from default import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("api/make", views.get_make, name="get_make"),
    path("api/model", views.get_model, name="get_model"),
    path("api/car-details", views.get_details, name="get_details"),
    path("api/price-prediction", views.score_data, name="score_data"),
]
