import random
from .models import AllInOneAccessibility

def admin_AIOA(request):
    try:
        
        color_code = ''
        license_key = ''
        aioa_place = ''
        aioa_icon_type = ''
        aioa_icon_size = ''

        script_url = (
            'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js'
            f'?colorcode={color_code}&token={license_key}&t={random.randint(0, 999999)}'
            f'&position={aioa_place}.{aioa_icon_type}.{aioa_icon_size}'
        )

        return {'AIOA_URL': script_url}
    
    except Exception as e:
        # Optional: log the error
        return {}
