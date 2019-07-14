from rest_framework import serializers
from apps.geography.models import Taxonomy, Destination
from apps.geography.api.serializers import DestinationSerializer as DestinationSerializerS


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
        extra_fields = []

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(DestinationSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def to_representation(self, instance):
        self.fields['taxonomy'] = TaxonomySerializer(read_only=True)
        self.fields['parent'] = DestinationSerializerS(read_only=True)
        return super(DestinationSerializer, self).to_representation(instance)
