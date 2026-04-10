import requests
from urllib.parse import urlparse

from django.contrib import admin
from django import forms
from django.shortcuts import redirect
from django.urls import reverse

from .models import AllinOneAccessibility, ICON_CHOICES, AIOA_ICON_SIZE_CHOICES
from .forms import IconSelectWidget, IconSizeSelectWidget


class AllinOneAccessibilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon_value = self.initial.get('aioa_icon_type') or self.instance.aioa_icon_type
        icon_url = dict(ICON_CHOICES).get(icon_value, '')
        self.fields['aioa_icon_size'].widget = IconSizeSelectWidget(
            choices=AIOA_ICON_SIZE_CHOICES,
            icon_url=icon_url
        )

    class Meta:
        model = AllinOneAccessibility
        fields = '__all__'
        widgets = {
            'aioa_icon_type': IconSelectWidget(choices=ICON_CHOICES),
        }


class AllinOneAccessibilityAdmin(admin.ModelAdmin):
    form = AllinOneAccessibilityForm

    fieldsets = (
        (None, {
            'fields': (
                'aioa_color_code',
                'enable_widget_icon_position',
                'to_the_right_px',
                'to_the_right',
                'to_the_bottom_px',
                'to_the_bottom',
                'aioa_place',
                'aioa_size',
                'aioa_icon_type',
                'enable_icon_custom_size',
                'aioa_size_value',
                'aioa_icon_size',
            )
        }),
    )

    class Media:
        js = ('admin/js/aioa_accessibility.js', 'admin/js/aioa_icon_sync.js')
        css = {'all': ('admin/css/aioa_admin.css',)}

    def has_add_permission(self, request):
        return not AllinOneAccessibility.objects.exists()

    def changelist_view(self, request, extra_context=None):
        """Redirect to single settings object, or show add page if none exists."""
        obj = AllinOneAccessibility.objects.first()
        if obj:
            return redirect(
                reverse('admin:accessibility_allinoneaccessibility_change', args=(obj.pk,))
            )
        return super().changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        """Saves settings and syncs to widget-setting-update-platform."""
        obj.save()

        domain = urlparse(request.build_absolute_uri())
        domain_url = f"{domain.scheme}://{domain.hostname}"

        data = {
            "u":                         domain_url,
            "widget_color_code":         obj.aioa_color_code,
            "is_widget_custom_position": int(obj.enable_widget_icon_position),
            "is_widget_custom_size":     int(obj.enable_icon_custom_size),
            "widget_icon_type":          obj.aioa_icon_type,
            "widget_size":               1 if obj.aioa_size == "oversize" else 0,
        }

        if not obj.enable_widget_icon_position:
            data.update({
                "widget_position_top":    None,
                "widget_position_right":  None,
                "widget_position_bottom": None,
                "widget_position_left":   None,
                "widget_position":        obj.aioa_place,
            })
        else:
            pos = {"top": None, "right": None, "bottom": None, "left": None}
            if obj.to_the_right == "to_the_left":
                pos["left"] = obj.to_the_right_px
            else:
                pos["right"] = obj.to_the_right_px
            if obj.to_the_bottom == "to_the_top":
                pos["top"] = obj.to_the_bottom_px
            else:
                pos["bottom"] = obj.to_the_bottom_px
            data.update({f"widget_position_{k}": v for k, v in pos.items()})
            data["widget_position"] = ""

        if not obj.enable_icon_custom_size:
            data.update({
                "widget_icon_size":        obj.aioa_icon_size,
                "widget_icon_size_custom": 0,
            })
        else:
            data.update({
                "widget_icon_size":        "",
                "widget_icon_size_custom": obj.aioa_size_value,
            })

        try:
            requests.post(
                "https://ada.skynettechnologies.us/api/widget-setting-update-platform",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        except Exception:
            pass  # Sync failure is non-fatal — settings are saved to DB regardless


admin.site.register(AllinOneAccessibility, AllinOneAccessibilityAdmin)
