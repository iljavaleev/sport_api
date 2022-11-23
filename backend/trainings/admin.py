from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'phone']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Role'), {'fields': ('is_student', 'is_coach')}),
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
    readonly_fields = ['last_login', 'created_at']
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ( 'email',
                        'password1',
                        'password2',
                        'is_coach',
                        'is_student',
                        'is_active',
                        'is_staff',
                        'is_superuser'
                        )
        }),
    )

class StudentAdmin(admin.ModelAdmin):
    model = models.Student
    ordering = ['username']
    list_display = ['get_student_email', 'get_student_phone']

    def get_student_email(self, obj):
        return obj.student.email

    def get_student_phone(self, obj):
        return obj.student.phone


class CoachAdmin(admin.ModelAdmin):
    model = models.Coach
    ordering = ['username']
    list_display = ['coach_email', 'coach_phone']


    def coach_email(self, obj):
        return obj.coach.email

    def coach_phone(self, obj):
        return obj.coach.phone


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Coach, CoachAdmin)
