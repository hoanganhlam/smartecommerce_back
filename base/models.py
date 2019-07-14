from django.db import models


class CoreModel(models.Model):

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __init__(self, *args, **kwargs):
        # super(getattr(sys.modules[__name__], self._meta.object_name), self).__init__(*args, **kwargs)
        super(CoreModel, self).__init__(*args, **kwargs)
        self.original_fiels = (self.__dict__).copy()

    class Meta:
        abstract = True


class CoreModelManager(models.Manager):
    pass


class CoreModelQuerySet(models.query.QuerySet):
    pass
