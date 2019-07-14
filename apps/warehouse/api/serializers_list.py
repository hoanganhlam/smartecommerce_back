from rest_framework import serializers
from apps.warehouse.models import Warehouse, Category, Taxonomy,\
    Product, Transaction, ProductInstance, Warehousing, Customer, Ordering, Order
from media.models import Media
from media.api.serializers_full import MediaSerializer
from authentication.api.serializers import UserSerializer
from django.db.models import Sum
from django.db.models import F, FloatField


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'


class ProductInstanceSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = ProductInstance
        fields = '__all__'
        extra_fields = ['name']

    def to_representation(self, instance):
        self.fields['photos'] = MediaSerializer(many=True, read_only=True)
        return super(ProductInstanceSerializer, self).to_representation(instance)

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ProductInstanceSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def get_name(self, instance):
        return '[' + instance.code + '] ' + instance.product.name

    def get_total(self, instance):
        return instance.transactions.aggregate(Sum('amount'))['amount__sum']


class ProductSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    instances = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'code': {'read_only': True}
        }
        extra_fields = ['photos', 'instances']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ProductSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(read_only=True)
        return super(ProductSerializer, self).to_representation(instance)

    def get_photos(self, instance):
        photos = Media.objects.filter(product_instances__product=instance)
        return MediaSerializer(photos, many=True).data

    def get_instances(self, instance):
        return ProductInstanceSerializer(instance.instances, many=True).data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        self.fields['product_instance'] = ProductInstanceSerializer(read_only=True)
        return super(TransactionSerializer, self).to_representation(instance)


class WarehousingSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    money = serializers.SerializerMethodField()

    class Meta:
        model = Warehousing
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        self.fields['warehouse'] = WarehouseSerializer(read_only=True)
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['transactions'] = TransactionSerializer(read_only=True, many=True)
        return super(WarehousingSerializer, self).to_representation(instance)

    def get_total(self, instance):
        return instance.transactions.aggregate(Sum('amount'))['amount__sum']

    def get_money(self, instance):
        return instance.transactions.aggregate(total=Sum(F('amount') * F('price_in'), output_field=FloatField()))[
            'total']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['customer'] = CustomerSerializer(read_only=True)
        self.fields['ordering'] = OrderingSerializer(read_only=True, many=True)
        return super(OrderSerializer, self).to_representation(instance)


class OrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordering
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product_instance'] = ProductInstanceSerializer(read_only=True)
        return super(OrderingSerializer, self).to_representation(instance)
