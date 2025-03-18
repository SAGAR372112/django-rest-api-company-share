from django.db import models
from customer_models import Customer
from account_models import Account
from transaction_models import Transaction


class LoanType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Base interest rate
    max_term_months = models.IntegerField()
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

class Loan(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('DISBURSED', 'Disbursed'),
        ('ACTIVE', 'Active'),
        ('PAID', 'Paid Off'),
        ('DEFAULTED', 'Defaulted'),
        ('CANCELLED', 'Cancelled'),
    )
    
    loan_number = models.CharField(max_length=20, unique=True)
    loan_type = models.ForeignKey(LoanType, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    disbursement_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='loan_disbursements')
    application_date = models.DateField(auto_now_add=True)
    approval_date = models.DateField(null=True, blank=True)
    disbursement_date = models.DateField(null=True, blank=True)
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    installment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    next_payment_date = models.DateField(null=True, blank=True)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2)
    total_payments_made = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    class Meta:
        indexes = [
            models.Index(fields=['loan_number']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
        ]

class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    principal_component = models.DecimalField(max_digits=15, decimal_places=2)
    interest_component = models.DecimalField(max_digits=15, decimal_places=2)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50)
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=True)
