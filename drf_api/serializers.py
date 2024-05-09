from rest_framework import serializers
from drf_api.models import VendorProfile,PurchaseOrder,VendorPerformance


class VendorProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = "__all__"
        

class PurchaseOrderSerailizers(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        
class VendorPerformanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = "__all__"
        
        
        
        
    