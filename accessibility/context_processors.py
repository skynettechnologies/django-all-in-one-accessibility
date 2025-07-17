import random
from .models import all_in_one_accessibility
from django.utils.html import format_html
from urllib.parse import urlparse

def admin_AIOA(request):
    domain = urlparse(request.build_absolute_uri())

    aioa_NOTE = "<span style='font-size:15px;' class='validate_pro'>Please <a href=""https://ada.skynettechnologies.us/trial-subscription?utm_source="+domain.netloc+"&utm_medium="+"django"+"-"+"packages"+"&utm_campaign=trial-subscription"" target=""_blank"">subscribe </a>for a 10 days free trial and receive a license key to enable 52+ features of All in One Accessibility Pro.<br>No payment charged upfront, Cancel anytime</span><script>if(document.querySelector('#id_aioa_license_Key').value != ''){document.querySelector('.validate_pro').style.display='none';} else {document.querySelector('.validate_pro').style.display='block';} </script>"
    
    aioa_BaseScript = ''
    
    all_in_one_accessibility._meta.get_field('aioa_license_Key').help_text = aioa_NOTE
    for a in all_in_one_accessibility.objects.all():        
        a_LK =a.aioa_license_Key.replace(']','').replace('[','').replace("'","")
        a_CC =a.aioa_color_code.replace(']','').replace('[','').replace("'","")
        a_AP =str(a.aioa_place).replace(']','').replace('[','').replace("'","")
        icon_type = str(a.aioa_icon_type)
        ICON = icon_type.replace(']','').replace('[','').replace("'","")
        icon_size = str(a.aioa_icon_size)
        SIZE = icon_size.replace(']','').replace('[','').replace("'","")
        
        if a_LK == '':
            pass            
        else:
            format_icon = ICON.split(',')
            value_i = format_icon[0]+".svg"
            format_size = SIZE.split(',')
            value_size = format_size[0]+".svg"
        
            aioa_BaseScript = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='+ a_CC + '&token=' + a_LK+'&t='+str(random.randint(0,999999))+'&position=' + a_AP+'.'+value_i+'.'+value_size
            
            all_in_one_accessibility._meta.get_field('aioa_icon_size').values = [('aioa-big-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]
                

    return {'AIOA_URL': aioa_BaseScript}



