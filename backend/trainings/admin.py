from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'first_name',
                           'last_name', 'role', 'sports_titles', 'weight',
                           'height', 'date_of_birth')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ( 'email',
                        'password',
                        'username',
                        'first_name',
                        'last_name',
                        'role',
                        'sports_titles',
                        'weight',
                        'height',
                        'date_of_birth',
                        'is_active',
                        'is_staff',
                        'is_superuser'
                        )
        }),
    )

admin.site.register(models.User, UserAdmin)
