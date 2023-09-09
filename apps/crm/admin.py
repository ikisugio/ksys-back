from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Jigyosyo, Company, LogicalJigyosyo, LogicalJigyosyoAction, AdminGroup, AdminUser

# Jigyosyo
@admin.register(Jigyosyo)
class JigyosyoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Jigyosyo._meta.fields]
    search_fields = ['name', 'address', 'company__name']
    list_filter = ['type', 'company']
    
    def company_link(self, obj):
        if obj.company:
            link = reverse("admin:crm_company_change", args=[obj.company.uuid])
            return format_html('<a href="{}">{}</a>', link, obj.company.name)
        return "No Company"
        
    company_link.short_description = 'Company'
    
    list_display = [field.name for field in Jigyosyo._meta.fields]
    list_display.append("company_link")
    list_display.remove('company')

# Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Company._meta.fields]
    search_fields = ['name', 'address', 'company_code']

# LogicalJigyosyo
FIELDS_TO_DISPLAY = [f.name for f in Jigyosyo._meta.fields if f.name != 'id']

@admin.register(LogicalJigyosyo)
class LogicalJigyosyoAdmin(admin.ModelAdmin):
    list_display = ['id'] + [f'representative_{field}' for field in FIELDS_TO_DISPLAY]
    search_fields = ['representative__name', 'representative__address', 'representative__company__name']
    list_filter = ['representative__type', 'representative__company']

    def __getattr__(self, name):
        if name.startswith('representative_'):
            field_name = name.split('representative_')[1]
            
            def wrapper(obj):
                attr = getattr(obj.representative, field_name)
                return attr() if callable(attr) else attr
            wrapper.short_description = field_name.replace('_', ' ').capitalize()
            return wrapper

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

# LogicalJigyosyoAction
@admin.register(LogicalJigyosyoAction)
class LogicalJigyosyoActionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LogicalJigyosyoAction._meta.fields]
    list_filter = ['action', 'created_at']
    search_fields = ['logical_jigyosyo__representative__name',]

# AdminGroup
@admin.register(AdminGroup)
class AdminGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdminGroup._meta.fields]
    search_fields = ['name',]
    list_filter = ['permission']

# AdminUser
@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AdminUser._meta.fields]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
