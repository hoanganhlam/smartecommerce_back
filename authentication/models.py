from django.contrib.auth.models import AbstractUser
from base.interface import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Permission(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Group(BaseModel):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(
        Permission,
        related_name='groups',
        blank=True,
    )

    def __str__(self):
        return self.name


class User(BaseModel, AbstractUser):
    groups = models.ManyToManyField(Group, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.username

    def get_group_permissions(self):
        return Permission.objects.filter(groups__in=self.groups.all()).distinct()

    def get_all_permissions(self):
        deny_ids = self.userpermission_set.filter(value = UserPermission.DENY)\
            .values_list('permission', flat=True)
        allow_ids = self.userpermission_set.filter(value = UserPermission.ALLOW)\
            .values_list('permission', flat=True)

        combined_permissions = self.get_group_permissions() | Permission.objects.filter(id__in = allow_ids).distinct()

        return combined_permissions.exclude(id__in=deny_ids).distinct()

    @property
    def permission_codes(self):
        return set(self.get_all_permissions().values_list('code', flat=True))


class UserPermission(BaseModel):
    DENY = -1
    INHERIT = 0
    ALLOW = 1
    PERMISSION_CHOICES = (
        (DENY, _('Deny')),
        (INHERIT, _('Inherit')),
        (ALLOW, _('Allow')),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=PERMISSION_CHOICES, default=INHERIT)

    def __str__(self):
        return '{} | {} | {}'.format(self.user.email, self.permission.name, self.get_value_display())

