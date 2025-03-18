from rest_framework import serializers
from .models import Company, UserLimit, Transaction

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'total_balance', 'available_balance']

class UserLimitSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    available_limit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = UserLimit
        fields = ['id', 'username', 'max_limit', 'used_amount', 'available_limit']

class TransactionSerializer(serializers.ModelSerializer):
    # No username field - users only see their own transactions
    user = serializers.CharField(source= 'user.username', read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'created_at']



class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']
        
    def create(self, validated_data):
        from .services import TransactionService
        
        user = self.context['request'].user
        amount = validated_data.get('amount')
        
        # Use the service to process the transaction
        transaction_service = TransactionService()
        transaction = transaction_service.process_transaction(user, amount)

        if transaction is None:
            raise serializers.ValidationError('Transaction could not be processed. Please check your limits.')
        return transaction
