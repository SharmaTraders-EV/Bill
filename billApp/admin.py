from django.contrib import admin
from .models import Product,Bill,CoustomersData

# Register your models here.
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(CoustomersData)