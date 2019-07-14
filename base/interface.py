from django.db import models
from django.core.paginator import Paginator
from django.db.models import Count


class BaseModel(models.Model):

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True


class NamedModel(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True


class AddressModel(models.Model):

    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    address = models.CharField(max_length=200)

    class Meta:
        abstract = True


class RateManager(models.Manager):
    def is_rated(self, user):
        return super().votes.objects.filter(owner=user).exists()

    def order_by_vote_count(self, **kwargs):
        return super().get_queryset().filter(**kwargs).annotate(count=Count('votes')).order_by('-count')

    def top_rate_count(self, size=10, **kwargs):
        lst = self.order_by_vote_count(**kwargs)
        paginator = Paginator(lst, size)
        return paginator.page(1)


class RatableModel(models.Model):
    objects = RateManager()

    def is_rated(self, user):
        if user.is_anonymous:
            return None
        check = self.rates.filter(user=user).first()
        if check:
            return check
        return None

    class Meta:
        abstract = True
