from rest_framework import viewsets, permissions
from base import pagination
from rest_framework.filters import OrderingFilter, SearchFilter
from apps.geography.models import Taxonomy, Destination
from apps.geography.api import serializers, serializers_list, serializers_full
from rest_framework.response import Response


class TaxonomyViewSet(viewsets.ModelViewSet):
    models = Taxonomy
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers.TaxonomySerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['name']
    lookup_field = 'pk'


class DestinationViewSet(viewsets.ModelViewSet):
    models = Destination
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_list.DestinationSerializer
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

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers_full.DestinationSerializer
        return super(DestinationViewSet, self).retrieve(request, *args, **kwargs)
