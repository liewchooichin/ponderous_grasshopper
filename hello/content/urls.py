from django.urls import path


from content import views as content_views


urlpatterns = [
    path(route="comment_form/", 
         view=content_views.comment_form,
         name="comment_form"),
    path(route="comment_done/",
         view=content_views.comment_done,
         name="comment_done"),
    path(route="ads_listing/",
          view=content_views.ads_listing,
          name="ads_listing"),
    path(route="put_an_ads/",
          view=content_views.put_an_ads,
          name="put_an_ads"),
    path(route="seeking_ads/create/",
         view=content_views.SeekingAdsGenericCreateView.as_view(),
         name="seeking_ads_generic_create_view"),
    path(route="seeking_ads/<int:pk>/", 
         view=content_views.SeekingAdsGenericUpdateView.as_view(),
         name="seeking_ads_generic_update_view"),
    path(route="seeking_ads/<int:pk>/delete/",
         view=content_views.SeekingAdsGenericDeleteView.as_view(),
         name="seeking_ads_generic_delete_view"),
    path(route="seekingad_delete_successful/",
         view=content_views.seekingad_delete_successful,
         name="seekingad_delete_successful"),
     path(route="user_edit_ads/",
          view=content_views.user_edit_ads,
          name="user_edit_ads"),
     path(route="edit_ads/<int:ad_id>/",
          view=content_views.put_an_ads,
          name="edit_ads"),
]

