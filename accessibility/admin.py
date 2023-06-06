from django.contrib import admin
from .models import all_in_one_accessibility


@admin.register(all_in_one_accessibility)
class ExampleModelAdmin(admin.ModelAdmin):
    
    # some code...
    list_display = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')
    list_display_links  = ('aioa_license_Key', 'aioa_color_code', 'aioa_place')

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and all_in_one_accessibility.objects.exists():
            retVal = False
        return retVal


