# hello/bands/urls.py

from django.urls import path

from bands import views as band_views

urlpatterns = [
    path(route="musician_detail/<int:musician_id>/", view=band_views.musician_detail, name="musician_detail"),
    path(route="musicians_list/", view=band_views.musicians_list, name="musicians_list"),
]

