from django.db import models

# Create your models here.
TENURE_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)

class OrderCreation(models.Model):
    asset_name  = models.CharField(max_length=20,null=True, blank=True)
    asset_value = models.FloatField(max_length=255,null=True, blank=True)
    MRP_value = models.FloatField(max_length=255,null=True, blank=True)

    tenure = models.CharField(max_length=255,choices = TENURE_CHOICES,null=True, blank=True)

    rental = models.FloatField(null=True, blank=True)
    refundable_security_deposit = models.FloatField(default=0,null=True, blank=True)
    insurance = models.FloatField(default=0,null=True, blank=True)

    monthly_rental = models.FloatField(null=True, blank=True)
    total_amount_payable = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.asset_name
    # class Meta:
    #     db_table = 'name'
