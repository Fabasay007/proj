from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser, Portfolio, PortfolioImage  # CustomUser

@admin.register(CustomerUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('age', 'avatar', 'phone_number')}),
    )
