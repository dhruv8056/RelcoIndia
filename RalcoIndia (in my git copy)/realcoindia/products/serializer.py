

from .models import OrderCreation
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCreation
        fields = ['id','asset_name','asset_value','MRP_value','tenure','rental','refundable_security_deposit','insurance','monthly_rental','total_amount_payable']


class ProductSerializer_For_customer(serializers.ModelSerializer):
    class Meta:
        model = OrderCreation
        fields = ['id','asset_name','tenure','refundable_security_deposit','insurance','monthly_rental','total_amount_payable']