from django.urls import path

from drf_api.views import (
    VendorProfileApiView,VendorProfileDetailApiView,
    PurchaseOrderAPIView,PurchaseOrderDetailAPIView,VendorPerformanceAPIView)

urlpatterns = [
    # Vendor Profile
    path('vendors/',VendorProfileApiView.as_view(),name='vendors'),
    path('vendors/<int:id>/',VendorProfileDetailApiView.as_view(),name='vendors_id'),
    
    # Purchase Order
    path('purchase_orders/',PurchaseOrderAPIView.as_view(),name='purchase_order'),
    path('purchase_orders/<int:id>/',PurchaseOrderDetailAPIView.as_view(),name='purchase_order_id'),
    
    # Vendor Performance
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name="vendor_performance"),
]

