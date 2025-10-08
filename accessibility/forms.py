
from django import forms
from django.utils.safestring import mark_safe

class IconSelectWidget(forms.Widget):
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None):
        output = ['<div class="icon-select-wrapper">']
        for option_value, icon_url in self.choices:
            checked = 'checked' if value == option_value else ''
            selected = 'selected' if value == option_value else ''
            output.append(f'''
                <label class="icon-option {selected}">
                    <input type="radio" name="{name}" value="{option_value}" {checked} hidden>
                    <img src="{icon_url}" alt="{option_value}" class="aioa-icon-img" />
                    <span class="checkmark">&#10004;</span>
                </label>
            ''')
        output.append('</div>')
        return mark_safe('\n'.join(output))
    


class IconSizeSelectWidget(forms.Widget):
    def __init__(self, attrs=None, icon_url='', choices=()):
        super().__init__(attrs)
        self.icon_url = icon_url  # this gets dynamically updated later
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None):
        size_map = {
            'aioa-big-icon': 75,
            'aioa-medium-icon': 65,
            'aioa-default-icon': 55,
            'aioa-small-icon': 45,
            'aioa-extra-small-icon': 35,
        }

        output = ['<div class="icon-size-select-wrapper">']
        for option_value, _ in self.choices:
            checked = 'checked' if value == option_value else ''
            selected = 'selected' if value == option_value else ''
            size = size_map[option_value]
            output.append(f'''
                <label class="icon-option {selected}" data-size="{size}">
                    <input type="radio" name="{name}" value="{option_value}" {checked} hidden>
                    <img src="{self.icon_url}" alt="{option_value}" style="width:{size}px;height:{size}px;" class="aioa-icon-img-size" />
                    <span class="checkmark">&#10004;</span>
                </label>
            ''')
        output.append('</div>')
        return mark_safe('\n'.join(output))


