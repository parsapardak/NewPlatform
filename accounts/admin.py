from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# حذف @admin.register اگر از قبل مدل ثبت شده است
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone', 'user_type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),
    )

# استفاده از admin.site.register فقط در صورتی که از قبل ثبت نشده باشد
try:
    admin.site.register(CustomUser, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    pass