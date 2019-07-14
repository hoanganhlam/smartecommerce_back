from django.contrib import admin
from .models import Warehouse, Product, ProductInstance, Category, Taxonomy
# Register your models here.

admin.site.register((Warehouse, Product, ProductInstance, Category, Taxonomy))
