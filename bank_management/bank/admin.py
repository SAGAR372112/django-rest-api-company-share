from django.contrib import admin
from .models import * 

# Register your models here.
@admin.register(Company)
class companyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_balance', 'available_balance')
    
@admin.register(UserLimit)
class UserlimitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'max_limit', 'used_amount')
    search_fields = ('user',)

class transactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'created_at', 'updated_at', 'notes')
    list_filter = ('status', 'created_at')
    search_fields = ('notes', 'status',)


