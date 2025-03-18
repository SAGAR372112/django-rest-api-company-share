from django.db import models
from user_authentication_models import User

class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('I', 'Individual'),
        ('C', 'Corporate'),
    )
    
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('S', 'Suspended'),
        ('B', 'Blacklisted'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    customer_id = models.CharField(max_length=20, unique=True)
    customer_type = models.CharField(max_length=1, choices=CUSTOMER_TYPES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    risk_level = models.CharField(max_length=10, default='MEDIUM')
    customer_since = models.DateField(auto_now_add=True)
    tax_id = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.customer_id} - {self.user.get_full_name()}"

class CustomerDocument(models.Model):
    DOCUMENT_TYPES = (
        ('PASSPORT', 'Passport'),
        ('DRIVING_LICENSE', 'Driving License'),
        ('NATIONAL_ID', 'National ID'),
        ('UTILITY_BILL', 'Utility Bill'),
    )
    
    VERIFICATION_STATUS = (
        ('P', 'Pending'),
        ('V', 'Verified'),
        ('R', 'Rejected'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=100)
    verification_status = models.CharField(max_length=1, choices=VERIFICATION_STATUS, default='P')
    document_file = models.FileField(upload_to='customer_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('customer', 'document_type', 'document_number')
