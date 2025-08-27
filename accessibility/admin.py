from django.contrib import admin

# Register your models here.
from django import forms
from .models import AllInOneAccessibility
from django.utils.safestring import mark_safe
import requests
import json
from urllib.parse import urlparse


    
# Map each choice key to its image URL
ICON_IMAGE_URLS = {
    'aioa-icon-type-1': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-1.svg',
    'aioa-icon-type-2': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-2.svg',
    'aioa-icon-type-3': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-3.svg',
    'aioa-icon-type-4': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-4.svg',
    'aioa-icon-type-5': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-5.svg',
    'aioa-icon-type-6': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-6.svg',
    'aioa-icon-type-7': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-7.svg',
    'aioa-icon-type-8': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-8.svg',
    'aioa-icon-type-9': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-9.svg',
    'aioa-icon-type-10': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-10.svg',
    'aioa-icon-type-11': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-11.svg',
    'aioa-icon-type-12': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-12.svg',
    'aioa-icon-type-13': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-13.svg',
    'aioa-icon-type-14': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-14.svg',
    'aioa-icon-type-15': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-15.svg',
    'aioa-icon-type-16': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-16.svg',
    'aioa-icon-type-17': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-17.svg',
    'aioa-icon-type-18': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-18.svg',
    'aioa-icon-type-19': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-19.svg',
    'aioa-icon-type-20': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-20.svg',
    'aioa-icon-type-21': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-21.svg',
    'aioa-icon-type-22': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-22.svg',
    'aioa-icon-type-23': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-23.svg',
    'aioa-icon-type-24': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-24.svg',
    'aioa-icon-type-25': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-25.svg',
    'aioa-icon-type-26': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-26.svg',
    'aioa-icon-type-27': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-27.svg',
    'aioa-icon-type-28': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-28.svg',
    'aioa-icon-type-29': 'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-29.svg',
}
# admin.py

class IconImageRadioSelect(forms.RadioSelect):
    class Media:
        js = ('static/icon-radio.js',)  # load custom JS

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for index, (opt_value, opt_label) in enumerate(self.choices):
            selected = str(opt_value) == str(value)
            output.append(self.render_option(name, opt_value, selected))

        return mark_safe(f'''
            <div style="
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                max-width: 920px;
            ">
                {''.join(output)}
            </div>
        ''')

    def render_option(self, name, value, selected):
        image_url = ICON_IMAGE_URLS.get(str(value), '')

        border_color = '#137333' if selected else 'transparent'


        card_style = (
            'display:inline-block;text-align:center;margin:8px;padding:8px;'
            'border-radius:10px;border:2px solid {border_color} ;position:relative;'
            'min-width:130px !important; width:130px !important;height:130px;box-sizing:border-box;cursor:pointer;background:#3c007f;'
        )

        # Checkmark hidden unless selected
        checkmark_display = 'flex' if selected else 'none'

        checkmark_html = f'''
            <span class="icon-checkmark" style="
                position:absolute;
                top:-32px;
                right:-31px;
                width:20px;
                height:20px;
                background:#137333;
                color:white;
                font-size:14px;
                font-weight:bold;
                border-radius:50%;
                align-items:center;
                justify-content:center;
                z-index:2;
                display:{checkmark_display};
            ">✓</span>
        '''

        icon_html = f'''
            <div style="width:70px;height:70px;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;margin:0 auto;position:relative;top:17%;">
                <img src="{image_url}" width="65" height="65" style="z-index:1;" />
                {checkmark_html}
            </div>
        '''
        return mark_safe(f'''
            <label class="icon-radio" style="{card_style}">
                <input type="radio" name="{name}" value="{value}" {'checked' if selected else ''} style="display:none;" />
                {icon_html}
            </label>
        ''')
    

class IconSizeWidget(forms.RadioSelect):
    class Media:
        js = ('static/icon-radio.js',)  # JS to toggle checkmarks

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for index, (opt_value, opt_label) in enumerate(self.choices):
            selected = str(opt_value) == str(value)
            output.append(self.render_option(name, opt_value, opt_label, selected))

        return mark_safe(f'''
            <div style="display:flex;flex-wrap:wrap;gap:10px;max-width:920px;">
                {''.join(output)}
            </div>
        ''')

    def render_option(self, name, value, label, selected):
        size_px = {
            'aioa-big-icon': 75,
            'aioa-medium-icon': 65,
            'aioa-default-icon': 55,
            'aioa-small-icon': 45,
            'aioa-extra-small-icon': 35,
        }.get(value, 55)


        icon_type = 'aioa-icon-type-1'  
        image_url = f"https://www.skynettechnologies.com/sites/default/files/{icon_type}.svg"

        border_color = '#137333' if selected else 'transparent'
        

        card_style = (
            f'display:inline-block;text-align:center;margin:8px;padding:8px;'
            f'border-radius:10px;border:2px solid {border_color};position:relative;'
            f'min-width:130px !important;width:130px !important;height:130px;'
            f'box-sizing:border-box;cursor:pointer;background:#3c007f;'
        )

        label_class = 'icon-radio selected' if selected else 'icon-radio'
    
        checkmark_display = 'flex' if selected else 'none'

        checkmark_html = f'''
            <span class="icon-checkmark" style="
                position:absolute;
                top:-13px;
                right:-15px;
                width:20px;
                height:20px;
                background:#137333;
                color:white;
                font-size:14px;
                font-weight:bold;
                border-radius:50%;
                align-items:center;
                justify-content:center;
                z-index:2;
                display:{checkmark_display};
            ">✓</span>
        '''

        icon_html = f'''
            <div style="width:100%;height:100%;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto;position:relative;">
                <img class="csticontype" src="{image_url}" width="{size_px}" height="{size_px}" style="z-index:1; " />
                {checkmark_html}
            </div>
        '''

        return mark_safe(f'''
            <label class="icon-radio" style="{card_style}">
                <input type="radio" name="{name}" value="{value}" {'checked' if selected else ''} style="display:none;" />
                {icon_html}
                <br><span style="color:white;">{label}</span>
            </label>
        ''')

    
class AllInOneAccessibilityForm(forms.ModelForm):
    class Meta:
        model = AllInOneAccessibility
        fields = '__all__'
        widgets = {
            'aioa_place': forms.RadioSelect,
            'aioa_size': forms.RadioSelect,
            'aioa_icon_type': IconImageRadioSelect,
            'aioa_icon_size': IconSizeWidget,
            'to_the_right_px': forms.NumberInput(attrs={'min': 0, 'max': 250}),
            'to_the_bottom_px': forms.NumberInput(attrs={'min': 0, 'max': 250}),
            'aioa_size_value': forms.NumberInput(attrs={'min': 20, 'max': 150})
        }

    
        


class AllInOneAccessibilityAdmin(admin.ModelAdmin):
    change_form_template = 'admin/accessibility/change_form.html'  # Custom template
    form = AllInOneAccessibilityForm

    fieldsets = (
        (None, {
            'fields': (
                'aioa_color_code',
                'enable_widget_icon_position',
                ('to_the_right_px', 'to_the_right'),
                ('to_the_bottom_px', 'to_the_bottom'),
                'aioa_place',
                'aioa_size',
                'aioa_icon_type',
                'aioa_icon_size',
                'enable_icon_custom_size',
                'aioa_size_value',
                # add more fields here
            ),
        }),
    )

    def has_add_permission(self, request):
        # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and AllInOneAccessibility.objects.exists():
            retVal = False
        return retVal

    def save_model(self, request, obj, form, change):
        obj.save()
        domain = urlparse(request.build_absolute_uri())
        domain_url = domain.scheme +'://'+domain.netloc
        
        url = "https://ada.skynettechnologies.us/api/widget-setting-update-platform"
        # Build data conditionally
        data = {
            "u": domain_url,
            "widget_color_code": obj.aioa_color_code,
            "is_widget_custom_position": int(obj.enable_widget_icon_position), #Enable Precise accessibility widget icon position
            "is_widget_custom_size": int(obj.enable_icon_custom_size), #Enable Icon Custom Size
        }

        # Handle position settings based on enable_widget_icon_position
        if not obj.enable_widget_icon_position:
            data.update({
                "widget_position_top": 0,
                "widget_position_right": 0,
                "widget_position_bottom": 0,
                "widget_position_left": 0,
                "widget_position": obj.aioa_place, 
            })
            
        else:
            
            # Initialize position with 0
            widget_position = {
                "widget_position_top": 0,
                "widget_position_right": 0,
                "widget_position_bottom": 0,
                "widget_position_left": 0,
            }

            # Horizontal position
            if obj.to_the_right == "to_the_left":
                widget_position["widget_position_left"] = obj.to_the_right_px
            elif obj.to_the_right == "to_the_right":
                widget_position["widget_position_right"] = obj.to_the_right_px

            # Vertical position
            if obj.to_the_bottom == "to_the_bottom":
                widget_position["widget_position_bottom"] = obj.to_the_bottom_px
            elif obj.to_the_bottom == "to_the_top":
                widget_position["widget_position_top"] = obj.to_the_bottom_px

            data.update(widget_position)
            data["widget_position"] = ""  # aioa_place is ignored in custom mode

        
        # Handle icon size settings
        if not obj.enable_icon_custom_size:
            data.update({
                "widget_icon_size": obj.aioa_icon_size,
                "widget_icon_size_custom": 0,
            })
        else:
            data.update({
                "widget_icon_size": "",
                "widget_icon_size_custom": obj.aioa_size_value,
            })

        # Include remaining fields
        widget_size_value = 1 if obj.aioa_size == "oversize" else 0
        data.update({
            "widget_size": widget_size_value, # regular,oversize
            "widget_icon_type": obj.aioa_icon_type,
        })
        
        files=[
        
        ]
        headers = {}
        try:
            response = requests.request("POST", url, headers=headers, data=data, files=files)
            response.raise_for_status()  # Raise exception if error
        except requests.HTTPError as e:
            error_body = ""
            try:
                error_body = response.json()  # Try to parse JSON error
            except ValueError:
                error_body = response.text  # Fall back to plain text if not JSON

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context or {})
    

admin.site.register(AllInOneAccessibility, AllInOneAccessibilityAdmin)


