from rest_framework import serializers
from apps.geography.models import Taxonomy, Destination


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'
        extra_kwargs = {
            'label': {'read_only': True}
        }


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        extra_kwargs = {
            'label': {'read_only': True}
        }
