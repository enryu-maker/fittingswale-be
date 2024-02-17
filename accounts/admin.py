from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ['id','name', 'mobile_no', 'email','is_trusty','is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'mobile_no', 'pan_no', 'gst_no', 'pan_card', 'gst_certificate', 'role','groups')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2',"role",'is_staff','is_superuser','groups',),
        }),
    )
    search_fields = ['email', 'name', 'mobile_no', 'pan_no', 'gst_no', 'role']
    ordering = ['id']
    filter_horizontal = []

admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Settings)
admin.site.register(Coupons)
admin.site.register(StarCoins)
