from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

from barcode import EAN13
from io import BytesIO
from barcode.writer import ImageWriter
import barcode
from django.core.files import File

# Create your models here.

PRODUCT_SERVICE = (
    ("Product","Product"),
    ("Service","Service")
)

ITEM_UNIT = (
    ("Kg","Kg"),
    ("M","M")
)

ITEM_TYPE = (
    ("Sell","Sell"),
    ("Buy","Buy"),
    ("Both","Both")
)


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null = True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name

class Rack(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null = True)
    rack = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.rack


class Inventory(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    warehouse = models.CharField(max_length=200, null=True)
    sku = models.CharField(max_length=200)
    item_name = models.CharField(max_length=200)
    stock = models.CharField(max_length=200)
    racks = models.CharField(max_length=200, null=True)
    product_or_service = models.CharField(max_length=200, choices=PRODUCT_SERVICE, default="Product")
    price = models.CharField(max_length=200, null=True)
    unit_of_measurement =  models.CharField(max_length=300, choices=ITEM_UNIT, default="Kg", null=True)
    hsn_code = models.CharField(max_length=300)
    type = models.CharField(max_length=300, choices=ITEM_TYPE, default="Sell", null=True)
    tax = models.CharField(max_length=200, null=True)
    barcode = models.ImageField(upload_to='barcode/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.item_name

    def get_barcode(self):
        barcode_format = barcode.get_barcode_class('code128')
        my_barcode = barcode_format(self.sku, writer=ImageWriter())
        buffer = BytesIO()
        my_barcode.write(buffer)
        return self.barcode.save(f'{self.sku}.png', File(buffer), save=False)

    def save(self, *args, **kwargs):
        self.get_barcode()
        super(Inventory, self).save(*args, **kwargs)
