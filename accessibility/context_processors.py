import json
import random
from django.conf import settings
from .models import all_in_one_accessibility


def admin_AIOA(request):
    aioa_BaseScript = ''
    for a in all_in_one_accessibility.objects.all():
        aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a.aioa_color_code + '&token=' + a.aioa_license_Key+'&t='+str(random.randint(0,999999))+'&position=' + a.aioa_place
            
    return {'AIOA_URL': aioa_BaseScript}
