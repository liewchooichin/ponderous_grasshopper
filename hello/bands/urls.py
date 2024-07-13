# hello/bands/urls.py

from django.urls import path

from bands import views as band_views

urlpatterns = [
    path(route="bands/",
         view=band_views.band_index, name="band_index"),
    path(route="musician_detail/<int:musician_id>/", 
         view=band_views.musician_detail, name="musician_detail"),
    path(route="musicians-list/", 
         view=band_views.musicians_list, name="musicians-list"),
    path(route="bandgroup_detail/<int:bandgroup_id>/", 
         view=band_views.bandgroup_detail, name="bandgroup_detail"),
    path(route="bandgroups_list/", 
         view=band_views.bandgroups_list, name="bandgroups_list"),
    path(route="room_detail/<int:room_id>/",
         view=band_views.room_detail, name="room_detail"),
    path(route="venues_list/",
         view=band_views.venues_list, name="venues_list"),
     path(route="restricted_page/", 
          view=band_views.restricted_page, name="restricted_page"),
     path(route="musician_restricted/<int:musician_id>/", 
          view=band_views.musician_restricted, name="musician_restricted"),
     path(route="room_detail_form/<int:room_id>/", 
          view=band_views.RoomFormView.as_view(), name="room_detail_form"),
     path(route="room_create_form/", 
          view=band_views.RoomCreateView.as_view(), name="room_create_form"),
]

