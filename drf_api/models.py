from django.db import models
from django.db.models import Avg, Count

class VendorProfile(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False)
    contact_details = models.TextField(max_length=15, null=True, blank=False)
    address = models.TextField(max_length=70, null=True, blank=False)
    vendor_code = models.CharField(max_length=50, null=True, blank=False, unique=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=False)
    quality_rating_avg = models.FloatField(null=True, blank=False)
    average_response_time = models.FloatField(null=True, blank=False)
    fulfillment_rate = models.FloatField(null=True, blank=False)
    
    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        on_time_delivery_count = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
        self.on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        self.quality_rating_avg = self.purchaseorder_set.filter(status='completed').aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0

        response_times = self.purchaseorder_set.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.F('acknowledgment_date') - models.F('issue_date')
        ).aggregate(avg_response_time=Avg('response_time'))
        self.average_response_time = response_times['avg_response_time'].total_seconds() if response_times['avg_response_time'] else 0

        total_orders = self.purchaseorder_set.count()
        successful_orders = self.purchaseorder_set.filter(status='completed').count()
        self.fulfillment_rate = (successful_orders / total_orders) * 100 if total_orders > 0 else 0

        self.save()
        
    class Meta:
        db_table = 'vendor_profile'

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, null=True, blank=False)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(auto_now_add=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, null=True, blank=False)
    quality_rating = models.FloatField(null=True, blank=False)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.update_performance_metrics()
        
    class Meta:
        db_table = 'purchase_order'

class VendorPerformance(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=False)
    quality_rating_avg = models.FloatField(null=True, blank=False)
    average_response_time = models.FloatField(null=True, blank=False)
    fulfillment_rate = models.FloatField(null=True, blank=False)
    
    class Meta:
        db_table = 'vendor_performance'
