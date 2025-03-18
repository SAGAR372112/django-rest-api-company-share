from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Transaction, Company, UserLimit
from .serializers import (
    TransactionSerializer, CreateTransactionSerializer, 
    UserLimitSerializer, CompanySerializer
)

class TransactionViewSet(viewsets.ModelViewSet):
    """Create and view transactions"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTransactionSerializer
        return TransactionSerializer
    
    @action(detail=False, methods=['get'])
    def my_transactions(self, request):
        """Get current user's transaction history"""
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """View company details"""
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Company.objects.all()

class UserLimitViewSet(viewsets.ReadOnlyModelViewSet):
    """View user limits"""
    serializer_class = UserLimitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserLimit.objects.filter(user=user)
