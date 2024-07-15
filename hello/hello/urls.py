"""
URL configuration for hello project.

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
from django.conf import settings
from django.conf.urls.static import static

# from github template
from hello.core import views as hello_views

# from tutorial
from home import views as home_views

# hello/hello/urls.py
urlpatterns = [
    # added by the github template
    path(route="hello_world/", view=hello_views.index, name="hello_world"),
    # original admin site
    path('admin/', admin.site.urls, name="admin"),
    # added by the github template
    path("__reload__/", include("django_browser_reload.urls")),
    # for home - tutorial
    path(route="", view=home_views.index, name="index"),
    path(route="credits/", view=home_views.credits, name="credits"),
    path(route="about/", view=home_views.about, name="about"),
    path(route="version/", view=home_views.version, name="version"),
    path(route="news/", view=home_views.news, name="news"),
    # experiments
    path(route="experiment_escape/", view=home_views.experiment_escape, name="experiment_escape"),
    path(route="starter_bootstrap/", view=home_views.starter_bootstrap, name="starter_bootstrap"),
    # for bands
    # Registering all the URL routes in the bands app
    path("bands/", include("bands.urls")),
    # for authentication
    #path(route="accounts/password_reset/", 
    #     view=home_views.my_password_reset_view,
    #     name="my_password_reset_view"),
    path('accounts/', include('django.contrib.auth.urls')),
    # Include content app
    path("content/", include("content.urls")),
]


# Only serve uploaded files this way if you are in DEBUG=True mode.
# Add the new route returned by static() into urlpatterns.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
