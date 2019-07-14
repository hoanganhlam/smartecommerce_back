"""wnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', admin.site.urls),
    url(r'^v1/media/', include(('media.api.urls', 'api_media'), namespace='api_media')),
    url(r'^v1/auth/', include(('authentication.api.urls', 'api_auth'), namespace='api_auth')),
    url(r'^v1/auth/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^v1/geography/', include(('apps.geography.api.urls', 'api_fact'), namespace='api_geography')),
    url(r'^v1/warehouse/', include(('apps.warehouse.api.urls', 'api_fact'), namespace='api_warehouse')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
