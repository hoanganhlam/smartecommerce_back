from django.contrib import admin
from .models import Taxonomy, Destination
# Register your models here.

admin.site.register((Taxonomy, Destination))
