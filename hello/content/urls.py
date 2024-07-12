from django.urls import path

from content import views as content_views

urlpatterns = [
    path(route="comment_form/", 
         view=content_views.comment_form,
         name="comment_form"),
    path(route="comment_done/",
         view=content_views.comment_done,
         name="comment_done")
]
