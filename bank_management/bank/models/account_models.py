from django.db import models
from user_authentication_models import User
from customer_models import Customer

class Branch(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_branches')
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)  # Against base currency
    is_base_currency = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code

class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Annual interest rate
    min_balance = models.DecimalField(max_digits=15, decimal_places=2)
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_limit = models.IntegerField(default=0)  # 0 means unlimited
    withdrawal_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

class Account(models.Model):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('D', 'Dormant'),
        ('C', 'Closed'),
        ('F', 'Frozen'),
    )
    
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    current_balance = models.DecimalField(max_digits=19, decimal_places=4)
    available_balance = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    opened_date = models.DateField(auto_now_add=True)
    closed_date = models.DateField(null=True, blank=True)
    last_activity_date = models.DateTimeField(auto_now=True)
    is_joint_account = models.BooleanField(default=False)
    overdraft_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return self.account_number
    
    class Meta:
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
        ]

class JointAccountHolder(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='joint_holders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    joined_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('account', 'customer')
