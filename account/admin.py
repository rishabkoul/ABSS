from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'date_joined', 'last_login')
    ordering = ['-last_login']
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)

# Register your models here.
