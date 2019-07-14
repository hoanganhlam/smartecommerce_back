from django.db import models
from base.interface import BaseModel, NamedModel
from apps.geography.models import Destination
from authentication.models import User
from media.models import Media
from django.contrib.postgres.fields import JSONField


# Create your models here.


class Warehouse(BaseModel, NamedModel):
    destination = models.ForeignKey(
        Destination, on_delete=models.SET_NULL, related_name='products', null=True,
        blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=160)


class Category(BaseModel, NamedModel):
    label = models.CharField(max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)


class Taxonomy(BaseModel, NamedModel):
    label = models.CharField(max_length=20)


class Product(BaseModel, NamedModel):
    code = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    field = JSONField(blank=True, null=True)

    def save(self, **kwargs):
        # generate unique slug
        if self._state.adding:
            last = Product.objects.order_by('-id').first()
            pk = 1
            if last:
                pk = last.pk + 1
            self.code = self.category.label + '_' + str(pk)
        super(Product, self).save(**kwargs)


class ProductInstance(BaseModel):
    code = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='instances', on_delete=models.CASCADE)
    photos = models.ManyToManyField(Media, related_name='product_instances')
    price_in = models.FloatField(default=0)
    price_out = models.FloatField(default=0)
    taxonomies = models.ManyToManyField(Taxonomy, related_name='products')
    data = JSONField(blank=True, null=True)

    def save(self, **kwargs):
        # generate unique slug
        if self._state.adding:
            count = ProductInstance.objects.filter(product=self.product).count()
            pk = count + 1
            self.code = self.product.code + '_' + str(pk)
        super(ProductInstance, self).save(**kwargs)


class Transaction(BaseModel):
    product_instance = models.ForeignKey(ProductInstance, related_name='transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    price_in = models.FloatField(default=0)
    amount = models.IntegerField()


class Warehousing(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehousing', on_delete=models.CASCADE)
    transactions = models.ManyToManyField(Transaction, related_name='warehousing')
    user = models.ForeignKey(User, related_name='warehousing', on_delete=models.CASCADE)
    note = models.CharField(max_length=300, null=True, blank=True)


class Customer(BaseModel):
    phone = models.CharField(max_length=15)
    fullname = models.CharField(max_length=100)
    social_profiles = JSONField(null=True, blank=True)


class Order(BaseModel):
    STATUS_CHOICES = [
        ('NEW', 'Đơn mới'),
        ('CONFIRM', 'Chờ tiếp nhận'),
        ('CONFIRM', 'Chờ hàng'),
        ('PICKED', 'Đã lấy hàng'),
        ('SENT', 'Đã gửi hàng'),
        ('SENDING', 'Đang giao hàng'),
        ('RECEIVED', 'Đã giao hàng'),
        ('DONE', 'Đã đối soái'),
    ]

    staff = models.ForeignKey(User, related_name='start_orders', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    note = models.CharField(max_length=500, blank=True, null=True)
    note_delivery = models.CharField(max_length=500, blank=True, null=True)
    destination = models.ForeignKey(Destination, related_name='orders', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    address = models.CharField(max_length=200)
    discount = models.FloatField(default=0)
    prepaid = models.FloatField(default=0)
    delivery_cost = models.FloatField(default=0)
    pay_for_delivery = models.BooleanField(default=False)
    urban_delivery = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default='NEW', max_length=10)


class Ordering(models.Model):
    product_instance = models.ForeignKey(ProductInstance, on_delete=models.CASCADE, related_name='ordering')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordering')
    amount = models.IntegerField(default=1)
