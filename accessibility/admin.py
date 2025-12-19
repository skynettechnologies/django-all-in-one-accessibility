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
import threading
import base64
import os
import json
from datetime import datetime

# Custom form to inject widgets and pass selected icon to size preview
class AllInOneAccessibilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get icon image for current selection
        icon_value = self.initial.get('aioa_icon_type') or self.instance.aioa_icon_type
        icon_url = dict(ICON_CHOICES).get(icon_value, '')

        # Set icon-size widget with correct icon preview
        self.fields['aioa_icon_size'].widget = IconSizeSelectWidget(
            choices=AIOA_ICON_SIZE_CHOICES,
            icon_url=icon_url
        )
    def clean(self):
        cleaned_data = super().clean()

        # If precise positioning is disabled → force safe defaults
        if not cleaned_data.get('enable_widget_icon_position'):
            cleaned_data['to_the_right_px'] = 20
            cleaned_data['to_the_right'] = 'to_the_left'
            cleaned_data['to_the_bottom_px'] = 20
            cleaned_data['to_the_bottom'] = 'to_the_bottom'
           

        # If custom icon size is disabled → force safe defaults
        if not cleaned_data.get('enable_icon_custom_size'):
            cleaned_data['aioa_size_value'] = 50
            
        return cleaned_data

    class Meta:
        model = AllInOneAccessibility
        fields = '__all__'
        # Use custom radio-style widget for icon type
        widgets = {
            'aioa_icon_type': IconSelectWidget(choices=ICON_CHOICES),
        }

# Custom admin class to manage AllInOneAccessibility model
class AllInOneAccessibilityAdmin(admin.ModelAdmin):
 
    form = AllInOneAccessibilityForm
    # Group form fields into logical sections (only one section here)
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
    # Only allow a single instance of this model
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if AllInOneAccessibility.objects.exists():
            return False
        return True
    
    # Always redirect from changelist view to the single instance edit page
    def changelist_view(self, request, extra_context=None):
        obj = AllInOneAccessibility.objects.first()
        if obj:
            return redirect(
                reverse('admin:accessibility_allinoneaccessibility_change', args=(obj.pk,))
            )
        return super().changelist_view(request, extra_context)
    
    # Include custom JS and CSS in admin
    class Media:
        js = ('admin/js/aioa_accessibility.js',
              'admin/js/aioa_icon_sync.js')
        css = {
            'all': ('admin/css/aioa_admin.css',)
        }
    
    # Custom save behavior to send data to external API on save
    def save_model(self, request, obj, form, change):
        
        obj.save()
        # Get current domain from request URL
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
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
                "widget_position": obj.aioa_place, 
            })
            
        else:
            
            # Initialize position with 0
            widget_position = {
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
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
        # Send API request to external service (with fallback error handling)
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


FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")

def call_accessibility_apis_once(request):
    if os.path.exists(FLAG_FILE):
        return

    try:
        # 1 First API: get JSON country data
        headers = {}
        response = requests.get("https://ipapi.co/json/", headers=headers, timeout=5)
        in_eu = False
        if response.status_code == 200:
            in_eu = response.json().get("in_eu", False)

        # 2 Second API: register domain
        full_url = request.build_absolute_uri('/').rstrip('/')  
        parsed = urlparse(full_url)
        domain_url = f"{parsed.scheme}://{parsed.hostname}"       
        domain_name = parsed.hostname      
      
        payload = {
            "name": domain_name,
            "email": f"no-reply@{domain_name}",
            "company_name": "",
            "website": base64.b64encode(domain_url.encode()).decode(),
            "package_type": "free-widget",
            "start_date": datetime.utcnow().isoformat(),
            "end_date": "",
            "price": "",
            "discount_price": "0",
            "platform": "Django",
            "api_key": "",
            "is_trial_period": "",
            "is_free_widget": "1",
            "bill_address": "",
            "country": "",
            "state": "",
            "city": "",
            "post_code": "",
            "transaction_id": "",
            "subscr_id": "",
            "payment_source": "",
            "no_required_eu": 1 if not in_eu else 0
        }
     
        register_resp = requests.post("https://ada.skynettechnologies.us/api/add-user-domain", data=payload, headers=headers)
        # Save flag file so this never runs again
        with open(FLAG_FILE, "w") as f:
            json.dump({
                "called": True,
                "no_required_eu": 1 if not in_eu else 0 
            }, f)

    except Exception as e:
        error_content = str(e)


# ---------------- Patch changelist_view AFTER class definition ----------------
original_changelist_view = AllInOneAccessibilityAdmin.changelist_view

def patched_changelist_view(self, request, extra_context=None):
    # Run API in background thread, only once
    threading.Thread(target=call_accessibility_apis_once, args=(request,), daemon=True).start()

    # Call original changelist view
    return original_changelist_view(self, request, extra_context)

# Patch the method directly
AllInOneAccessibilityAdmin.changelist_view = patched_changelist_view

# Register the model with the custom admin class
admin.site.register(AllInOneAccessibility, AllInOneAccessibilityAdmin)
