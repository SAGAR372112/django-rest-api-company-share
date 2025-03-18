from decimal import Decimal
from .models import Company, UserLimit, Transaction
from django.db import transaction

class TransactionService:
    """
    Service class for handling transaction business logic
    """
    
    def process_transaction(self, user, amount):
        """
        Process a new transaction with validation and updates
        """
        company = Company.objects.first()  # Assuming one company for simplicity
        
        try:
            user_limit = UserLimit.objects.get(user=user)
            
            # Validate user limit
            available_limit = self._calculate_available_limit(user_limit)
            if amount > available_limit:
                return None
            
            # Validate company balance
            if amount > company.available_balance:
                return None
            
            # Process valid transaction
            with transaction.atomic():
                # Create transaction record
                new_transaction = Transaction(
                    user=user,
                    company=company,
                    amount=amount
                )
                new_transaction.save()
                
                # Update user limit
                user_limit.used_amount += amount
                user_limit.save()
                
                # Update company balance
                company.available_balance -= amount
                company.save()
                
                return new_transaction
        
        except UserLimit.DoesNotExist:
            return None
    
    def _calculate_available_limit(self, user_limit):
        """
        Calculate the available limit for a user
        """
        return max(Decimal('0'), user_limit.max_limit - user_limit.used_amount)

class UserLimitService:
    """
    Service class for user limit operations
    """
    def calculate_available_limit(self, user_limit):
        """
        Calculate the available limit for a user
        """
        return max(Decimal('0'), user_limit.max_limit - user_limit.used_amount)