from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from address.models import Address
# Register your models here.

class AddressAdmin(ImportExportModelAdmin):
    list_display=('state','district','subdistrict','officename','villagename','pincode')

admin.site.register(Address,AddressAdmin)

