from django.db import models
from base.interface import BaseModel, AddressModel, NamedModel
from utils.slug import unique_slugify


# Create your models here.


class Taxonomy(BaseModel, NamedModel):
    label = models.CharField(max_length=200)

    def save(self, **kwargs):
        # generate unique slug
        unique_slugify(self, slug_field_name='label', value=self.name)
        super(Taxonomy, self).save(**kwargs)


class Destination(BaseModel, NamedModel, AddressModel):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='destinations', null=True,
                                 blank=True)
    label = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def save(self, **kwargs):
        # generate unique slug
        unique_slugify(self, slug_field_name='label', value=self.name)
        super(Destination, self).save(**kwargs)
