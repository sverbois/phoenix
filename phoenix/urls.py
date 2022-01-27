"""phoenix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic.base import RedirectView

from .views import contact_view

urlpatterns = [
    path("", RedirectView.as_view(url="/coaching/"), name="redirect-to-coaching-home"),
    path("contact/", contact_view, name="contact"),
    path("coaching/", include("coaching.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "accounts/profile/",
        RedirectView.as_view(url="/coaching/dashboard"),
        name="redirect-to-coaching-dashboard",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
