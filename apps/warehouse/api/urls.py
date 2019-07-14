from apps.warehouse.api import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'warehouses', views.WarehouseViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'taxonomies', views.TaxonomyViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product-instances', views.ProductInstanceViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'warehousing', views.WarehousingViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'ordering', views.OrderingViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
