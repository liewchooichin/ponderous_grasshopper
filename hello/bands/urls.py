# hello/bands/urls.py

from django.urls import path

from bands import views as band_views
from home import views as home_views
from bands.forms import VenueForm, RoomForm


urlpatterns = [
    path(route="bands/",
         view=home_views.index, name="index"),
    path(route="musician_detail/<int:musician_id>/", 
         view=band_views.musician_detail, name="musician_detail"),
    path(route="musicians_list/", 
         view=band_views.musicians_list, name="musicians_list"),
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
     path(route="venue_add/0/",
          view=band_views.venue_edit, name="venue_add"),
     path(route="venue_edit/<int:venue_id>/",
          view=band_views.venue_edit, name="venue_edit"),
     path(route="user_profile/",
          view=band_views.display_userprofile, name="user_profile"),
     path(route="user_add_musician/<int:musician_id>/", 
          view=band_views.user_edit_musician, name="user_add_musician"),
     path(route="user_edit_musician/<int:musician_id>/", 
          view=band_views.user_edit_musician, name="user_edit_musician"),
     path(route="user_list_musician", 
          view=band_views.user_list_musician, 
          name="user_list_musician"),

]

