# Register your models here.
from django.contrib import admin
from .models import AllInOneAccessibility
from django import forms
from .models import AllInOneAccessibility, ICON_CHOICES, AIOA_ICON_SIZE_CHOICES
from .forms import IconSelectWidget, IconSizeSelectWidget
from urllib.parse import urlparse
import requests
from django.shortcuts import redirect
from django.urls import reverse

class AllInOneAccessibilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get icon image for current selection
        icon_value = self.initial.get('aioa_icon_type') or self.instance.aioa_icon_type
        icon_url = dict(ICON_CHOICES).get(icon_value, '')

        self.fields['aioa_icon_size'].widget = IconSizeSelectWidget(
            choices=AIOA_ICON_SIZE_CHOICES,
            icon_url=icon_url
        )

    class Meta:
        model = AllInOneAccessibility
        fields = '__all__'
        widgets = {
            'aioa_icon_type': IconSelectWidget(choices=ICON_CHOICES),
        }


class AllInOneAccessibilityAdmin(admin.ModelAdmin):

    form = AllInOneAccessibilityForm

    fieldsets = (
        (None, {
            'fields': (
                'aioa_color_code',
                'enable_widget_icon_position',
                ('to_the_right_px', 'to_the_right'),  # ← Inline row
                ('to_the_bottom_px', 'to_the_bottom'),  # ← Inline row
                'aioa_place',
                'aioa_size',
                'aioa_icon_type',
                'enable_icon_custom_size',
                'aioa_size_value',
                'aioa_icon_size',
            )
        }),
    )
   
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if AllInOneAccessibility.objects.exists():
            return False
        return True
    
    def changelist_view(self, request, extra_context=None):
        obj = AllInOneAccessibility.objects.first()
        if obj:
            return redirect(
                reverse('admin:accessibility_allinoneaccessibility_change', args=(obj.pk,))
            )
        return super().changelist_view(request, extra_context)
    
    class Media:
        js = ('admin/js/aioa_accessibility.js',
              'admin/js/aioa_icon_sync.js')
        css = {
            'all': ('admin/css/aioa_admin.css',)
        }
    
    def save_model(self, request, obj, form, change):
        
        obj.save()
        domain = urlparse(request.build_absolute_uri())
        domain_url = f"{domain.scheme}://{domain.hostname}"
        
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
        url = "https://ada.skynettechnologies.us/api/widget-setting-update-platform"
        try:
            response = requests.request("POST", url, headers=headers, data=data, files=files)
            response.raise_for_status()
        except requests.RequestException as e:
            if response is not None:
                try:
                    error_content = response.json()
                except Exception:
                    error_content = response.text
            else:
                error_content = str(e)

# Register the model with the custom admin class
admin.site.register(AllInOneAccessibility, AllInOneAccessibilityAdmin)
