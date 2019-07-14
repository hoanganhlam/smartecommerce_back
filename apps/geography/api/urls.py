from apps.geography.api import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'taxonomies', views.TaxonomyViewSet)
router.register(r'destinations', views.DestinationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
