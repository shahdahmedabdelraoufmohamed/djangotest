from django.contrib import admin
from .models import PurchaseOrder , PurchaseOrderLine , Supplier , Product
# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
admin.site.register(Supplier)
admin.site.register(Product)