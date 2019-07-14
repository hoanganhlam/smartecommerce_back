# from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from base import pagination
from . import serializers_full
from media.models import Media
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
# from datetime import datetime


class MediaViewSet(viewsets.ModelViewSet):
    models = Media
    queryset = models.objects.all().order_by('id')
    serializer_class = serializers_full.MediaSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', ]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers_full.MediaSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        is_browser = request.GET.get('browser')
        if is_browser:
            self.queryset = self.queryset.filter(user=request.user)
        return super(MediaViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        self.parser_classes = (MultiPartParser,)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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