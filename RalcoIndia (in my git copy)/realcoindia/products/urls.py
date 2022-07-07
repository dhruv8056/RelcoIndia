from django.urls import path
from .views import ProductsForAdmin,ProductsForCustomer
from rest_framework.schemas import get_schema_view

from django.views.generic import TemplateView

urlpatterns = [
    #admin_side_view
    path('admin_side_product',ProductsForAdmin.as_view(),name='ProductsForAdmin'),
    path('admin_side_product/<int:pk>/', ProductsForAdmin.as_view(),name='ProductsForAdmin'),

    #for_customer
    path('customer_side_product',ProductsForCustomer.as_view(),name='ProductsForAdmin'),
    path('customer_side_product/<int:pk>/', ProductsForCustomer.as_view(),name='ProductsForAdmin'),
] 