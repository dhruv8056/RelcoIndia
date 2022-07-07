import re
from django.shortcuts import render
from uritemplate import partial
from .serializer import ProductSerializer,ProductSerializer_For_customer
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from  rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAdminUser
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
# Create your views here.

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin) 

class ProductsForAdmin(APIView, SuperuserRequiredMixin):
    permission_classes= (IsSuperUser, ) 
    def get_object(self, pk):
        try:
            return OrderCreation.objects.get(pk=pk)
        except OrderCreation.DoesNotExist:
            raise Http404
 
    def get(self, request, pk=None, format=None):
        if pk:
            assignment = OrderCreation.objects.get(id=pk)
            serializer = ProductSerializer(assignment)
            return Response(serializer.data)
            
        Products_data = OrderCreation.objects.all().order_by('MRP_value')
        serializer = ProductSerializer(Products_data,many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        create a Products.
        """
        Products_data = request.data
        if request.data.get('asset_value'):

            asset_value = request.data.get('asset_value')

            monthly_rental = float(request.data.get('asset_value')) /10 * float(request.data.get('tenure'))

            total_amount_payable = monthly_rental + float(request.data.get('insurance')) + float(request.data.get('refundable_security_deposit'))

        databasesave = OrderCreation(monthly_rental=monthly_rental,total_amount_payable=total_amount_payable)
        databasesave.save()

        Products_data.pop('monthly_rental')
        Products_data.pop('total_amount_payable')         
                                                  
        serializer = ProductSerializer(instance=databasesave, data=Products_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            assignment_saved = serializer.save()   
        return Response({"success": "Products created successfully"})

    def put(self, request, pk, format=None):
        """
        update a Products.
        """
        assignment = OrderCreation.objects.get(id=pk)
        serializer = ProductSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response({"success": "Products deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class ProductsForCustomer(APIView):
    permission_classes= (AllowAny, ) 
    # def get_object(self, pk):
    #     try:
    #         return OrderCreation.objects.get(pk=pk)
    #     except OrderCreation.DoesNotExist:
    #         raise Http404
 
    def get(self, request, pk=None, format=None):   
        try:
            if pk:
                assignment = OrderCreation.objects.get(id=pk)
                serializer = ProductSerializer_For_customer(assignment)
                return Response(serializer.data)
        except OrderCreation.DoesNotExist:
            print("------------------not id_-------------")
            return Response({"error": "ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        else:
            Products_data = OrderCreation.objects.all().order_by('MRP_value')
            serializer = ProductSerializer_For_customer(Products_data,many=True)
            return Response(serializer.data)