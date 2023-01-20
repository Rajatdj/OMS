from django.contrib import admin
from .models import Inventory, Category, Warehouse, Rack
# Register your models here.

admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(Warehouse)
admin.site.register(Rack)