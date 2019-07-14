from rest_framework import serializers
from authentication.models import User
from rest_auth.registration.serializers import RegisterSerializer
from media.api.serializers_full import MediaSerializer


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'avatar',
            'id',
            'username',
            'address',
            'email',
            'phone',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined']

    def get_avatar(self, instance):
        image = instance.medias.filter(is_avatar=True).first()
        return MediaSerializer(image).data


class NameRegistrationSerializer(RegisterSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])
