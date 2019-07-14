from django.db import models
from authentication.models import User
from sorl.thumbnail import ImageField
import os
from uuid import uuid4
import datetime
from sorl.thumbnail import delete
from base.interface import BaseModel
from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size

    if file_size > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def path_and_rename(instance, filename):
    now = datetime.datetime.now()
    upload_to = 'images/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.


class Tag(BaseModel):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True)


class Media(BaseModel):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True)
    file = ImageField(upload_to=path_and_rename, max_length=500, validators=[validate_file_size])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='medias', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="medias")
    is_avatar = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        delete(self.file)
        super(Media, self).delete(*args, **kwargs)

    def __str__(self):
        return self.title
