from urllib.parse import urlparse
from django.contrib import admin
import requests
from .models import all_in_one_accessibility
from django.contrib import messages


class aioa_admin_form(admin.ModelAdmin):
    
    # list_display = ('aioa_license_Key', 'aioa_color_code', 'aioa_place','aioa_icon_type','aioa_icon_size')
    # list_display_links  = ('aioa_license_Key', 'aioa_color_code', 'aioa_place','aioa_icon_type','aioa_icon_size')

            # print()

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and all_in_one_accessibility.objects.exists():
            retVal = False
        return retVal

   
    # def get_fields(self, request, obj=''):
    #     print(all_in_one_accessibility.objects.all())
        
        # for data in all_in_one_accessibility.objects.all():
        #     if data.aioa_license_Key != '':
        #         return ('aioa_license_Key', 'aioa_color_code', 'aioa_place','aioa_icon_type','aioa_icon_size')
        #     return ('aioa_license_Key', 'aioa_color_code', 'aioa_place')

    def save_model(self, request, obj, form, change):
        super(aioa_admin_form, self).save_model(request, obj, form, change)
        for data in all_in_one_accessibility.objects.all():
            domain = urlparse(request.build_absolute_uri())
            domain_url = domain.scheme +'://'+domain.netloc
            print(domain_url)
            url = "https://ada.skynettechnologies.us/api/widget-setting-update-platform"

            payload = {'u': domain_url,
            'widget_position': data.aioa_place,
            'widget_color_code': data.aioa_color_code,
            'widget_icon_type': data.aioa_icon_type,
            'widget_icon_size': data.aioa_icon_size}
            files=[

            ]
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

        
        super().save_model(request, obj, form, change)
admin.site.register(all_in_one_accessibility, aioa_admin_form)