from django.contrib import admin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUser_reg(admin.ModelAdmin):
    list_display = ['id','mobile_number','email','FCM','id']