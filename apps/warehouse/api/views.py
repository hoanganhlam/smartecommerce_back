from rest_framework import viewsets, permissions
from base import pagination
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.warehouse.models import Warehouse, Category, Taxonomy, \
    Product, Transaction, ProductInstance, Warehousing, Order, Ordering, Customer
from apps.warehouse.api import serializers, serializers_list, serializers_full
from rest_framework.response import Response


class WarehouseViewSet(viewsets.ModelViewSet):
    models = Warehouse
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers.WarehouseSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    models = Category
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers.CategorySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TaxonomyViewSet(viewsets.ModelViewSet):
    models = Taxonomy
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers.TaxonomySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    models = Product
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.ProductSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ProductInstanceViewSet(viewsets.ModelViewSet):
    models = ProductInstance
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.ProductInstanceSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['product__name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    models = Transaction
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.TransactionSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WarehousingViewSet(viewsets.ModelViewSet):
    models = Warehousing
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.WarehousingSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerViewSet(viewsets.ModelViewSet):
    models = Customer
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.CustomerSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    lookup_field = 'pk'
    search_fields = ['phone', 'fullname']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    models = Order
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.OrderSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderingViewSet(viewsets.ModelViewSet):
    models = Ordering
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.OrderingSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
