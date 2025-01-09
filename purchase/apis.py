from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (SupplierSerializer, ProductSerializer, 
                         PurchaseOrderSerializer)
from .models import Supplier, Product, PurchaseOrder
from django_filters import rest_framework as filters
from rest_framework import status

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        # Implement validation logic before deletion
        pass
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    # Implement custom actions if needed


class PurchaseOrderFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='order_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='order_date', lookup_expr='lte')
    status = filters.ChoiceFilter(field_name='status', choices=PurchaseOrder.STATUS_CHOICES)

    class Meta:
        model = PurchaseOrder
        fields = ['start_date', 'end_date', 'status']

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PurchaseOrderFilter
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        
        # methods for: 1)status transition validation
        
        purchase_order = self.get_queryset().filter(pk=pk).first()
        new_status = request.data.get('status')
        if purchase_order.status == 'COMPLETED':
            return Response({"msg": "This Purchase Order is already completed."},status=status.HTTP_400_BAD_REQUEST)
        valid_transitions = {
            'DRAFT': ['SUBMITTED'],      
            'SUBMITTED': ['APPROVED'],   
            'APPROVED': ['COMPLETED'],    
            'COMPLETED': []            
        }

        if new_status in valid_transitions[purchase_order.status]:
            purchase_order.status = new_status
            purchase_order.save()
            return Response({"msq": "Status updated successfully.", "new_status": new_status},status=status.HTTP_200_OK)
        else:
            return Response({"msg": f"Cannot transition from {purchase_order.status} to {new_status}."},status=status.HTTP_400_BAD_REQUEST )