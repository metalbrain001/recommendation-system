from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin class to handle user-related fields, permissions,
    and customize the admin interface for the User model.
    """

    # Specify how the users should be ordered
    ordering = ['id']

    # Fields to display in the list view of the User model
    list_display = ['email', 'name', 'is_staff', 'is_active']

    # Custom fieldset for viewing and editing user details
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    # Custom fieldset for adding a new user, with password confirmation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

    # Search functionality for easy lookup of users
    search_fields = ['email', 'name']

    # Filters for narrowing down the list view in the admin interface
    list_filter = ['is_staff', 'is_active', 'is_superuser']

    # Set readonly fields to prevent modification of certain fields
    readonly_fields = ['last_login']


# Register the User model with the customized UserAdmin class
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Movie)
admin.site.register(models.Ratings)
admin.site.register(models.Tags)
