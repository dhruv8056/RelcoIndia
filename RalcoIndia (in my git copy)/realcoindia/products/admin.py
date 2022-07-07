from django.contrib import admin

# Register your models here.
from .models import OrderCreation
# Register your models here.

@admin.register(OrderCreation)
class Products_register(admin.ModelAdmin):
    list_display = ['id','asset_name','asset_value','MRP_value','tenure','rental','refundable_security_deposit','insurance','monthly_rental','total_amount_payable']