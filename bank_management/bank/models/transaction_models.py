from django.db import models
from account_models import Account, Currency
from user_authentication_models import User


class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    affects_balance = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Reversed'),
    )
    
    transaction_id = models.CharField(max_length=30, unique=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    source_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='outgoing_transactions', null=True)
    destination_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='incoming_transactions', null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    value_date = models.DateField()  # When the transaction affects the balance
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    reference_number = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_transactions')
    authorized_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='authorized_transactions', null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['source_account']),
            models.Index(fields=['destination_account']),
            models.Index(fields=['transaction_date']),
            models.Index(fields=['status']),
        ]

class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    )
    
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('P', 'Paused'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    )
    
    source_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurring_debits')
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurring_credits')
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_execution = models.DateTimeField(null=True, blank=True)
    next_execution = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
