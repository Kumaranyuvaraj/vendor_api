from django.shortcuts import render
from drf_api.models import VendorProfile,PurchaseOrder,VendorPerformance
from drf_api.serializers import VendorProfileSerializers,PurchaseOrderSerailizers,VendorPerformanceSerializers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication


# Vendor Profile Management

class VendorProfileApiView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def post(self, request):
        serializer = VendorProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        vendor_profiles = VendorProfile.objects.all()
        serializer = VendorProfileSerializers(vendor_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorProfileDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get_object(self, id):
        try:
            return VendorProfile.objects.get(id=id)
        except VendorProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        vendor_profile = self.get_object(id)
        serializer = VendorProfileSerializers(vendor_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        vendor_profile = self.get_object(id)
        serializer = VendorProfileSerializers(vendor_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        vendor_profile = self.get_object(id)
        vendor_profile.delete()
        return Response({'Message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
    

# Purchase Order Tracking

class PurchaseOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
     
    def post(self, request):
        serializer = PurchaseOrderSerailizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerailizers(purchase_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PurchaseOrderDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
     
    def get_object(self, id):
        try:
            return PurchaseOrder.objects.get(id=id)
        except PurchaseOrder.DoesNotExist:
            raise Http404
    
    def get(self, request, id):
        purchase_order = self.get_object(id)
        serializer = PurchaseOrderSerailizers(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        purchase_order = self.get_object(id)
        serializer = PurchaseOrderSerailizers(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        purchase_order = self.get_object(id)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class VendorPerformanceAPIView(APIView):
    authentication_classes = [JWTAuthentication]
     
    def get(self, request, vendor_id):
        try:
            vendor_profiles = VendorProfile.objects.get(id=vendor_id)
            serializer = VendorProfileSerializers(vendor_profiles)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorProfile.DoesNotExist:
            return Response({'error': 'Vendor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
            
    
    
