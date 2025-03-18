from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2)
    available_balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.name

    def update_available_balance(self, amount):
        self.available_balance += amount
        self.save()

class UserLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='limit')
    max_limit = models.DecimalField(max_digits=10, decimal_places=2)
    used_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def available_limit(self):
        return self.max_limit - self.used_amount
    
    def __str__(self):
        return f"{self.user.username}'s limit"

    def update_used_amount(self, amount):
        self.used_amount += amount
        self.save()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.company.name} - {self.amount}"

    def save(self, *args, **kwargs):
        try:
            if self.user.limit.available_limit < self.amount:
                raise ValueError("User limit exceeded")
            if self.company.available_balance < self.amount:
                raise ValueError("Company balance insufficient")
            self.user.limit.update_used_amount(self.amount)
            self.company.update_available_balance(-self.amount)
            super().save(*args, **kwargs)
        except ValueError as e:
            raise e