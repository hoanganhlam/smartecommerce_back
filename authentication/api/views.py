from rest_framework import views, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.models import User
from authentication.api.serializers import UserSerializer
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework import viewsets, permissions
from base import pagination
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    models = User
    queryset = models.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.CustomPagination
    filter_backends = [OrderingFilter]
    search_fields = ['first_name', 'last_name', 'username']
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserSerializer
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)


class UserExt(views.APIView):
    @api_view(['GET'])
    @permission_classes((IsAuthenticated,))
    def get_request_user(request, format=None):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user, context={'request': request})
        response = serializer.data
        return Response(response, status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleConnect(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
