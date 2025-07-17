from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .db import RadioGridField
from django.db import models

aioa_SELECT_CHOICE = [('top_left','Top left'),
      ('top_center','Top Center'),
      ('top_right','Top Right'),
      ('middel_left','Middle left'),
      ('middel_right','Middle Right'),
      ('bottom_left','Bottom left'),
      ('bottom_center','Bottom Center'),
      ('bottom_right','Bottom Right')]

def validate_token(value):
    if value is not None:
        pass
    else:
        raise ValidationError("This field accepts mail id of google only")

ROWS = ((1 ,''),)

icon_change = '''    
    <script>
    const sizeOptions = document.querySelectorAll('input[name="aioa_icon_size_0"]');
    console.log(sizeOptions)
    const sizeOptionsImg = document.querySelectorAll('.csticontype');
    const typeOptions = document.querySelectorAll('input[name="aioa_icon_type_0"]');
    typeOptions.forEach(option => {
        option.addEventListener("click", (event) => {
            sizeOptionsImg.forEach(option2 => {
                var ico_type = document.querySelector('input[name="aioa_icon_type_0"]:checked').value;
                option2.setAttribute("src", "https://skynettechnologies.com/sites/default/files/python/" + ico_type + ".svg");
            });
        });
    });
</script>

<script>
      if(document.querySelector("#id_aioa_license_Key").value != '')
      {
          document.querySelector('div[class="form-row field-aioa_icon_type"]').style.display='block';
          document.querySelector('div[class="form-row field-aioa_icon_size"]').style.display='block';
          document.querySelector('div[class="form-row field-aioa_color_code"]').style.display='block';
          document.querySelector('div[class="form-row field-aioa_place"]').style.display='block';
      }
      else
      {
          document.querySelector('div[class="form-row field-aioa_icon_type"]').style.display='none';
          document.querySelector('div[class="form-row field-aioa_icon_size"]').style.display='none';
          document.querySelector('div[class="form-row field-aioa_color_code"]').style.display='none';
          document.querySelector('div[class="form-row field-aioa_place"]').style.display='none';
      }
      </script>  
'''

value_i = 'aioa-icon-type-1.svg'

CHOICES = [('aioa-icon-type-1', format_html('<img  src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />')), ('aioa-icon-type-2', format_html('<img  src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-2.svg" width="65" height="65" />')), ('aioa-icon-type-3', format_html('<img  src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-3.svg" width="65" height="65" />'))]

CHOICES1 = [('aioa-big-icon', format_html('<img class="csticontype"  src="https://skynettechnologies.com/sites/default/files/python/{}" width="75" height="75" />',value_i)), ('aioa-medium-icon', format_html('<img class="csticontype"src="https://skynettechnologies.com/sites/default/files/python/{}" width="65" height="65" />',value_i)), ('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), ('aioa-small-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="45" height="45" />',value_i)), ('aioa-extra-small-icon',format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="35" height="35"/>',value_i))]


class all_in_one_accessibility(models.Model):
    aioa_license_Key = models.CharField(max_length=150,blank=True,validators=[validate_token],default=None,verbose_name='License Key')
    
    aioa_color_code = models.CharField(max_length=50,blank=True,default=' ',verbose_name ='Hex color code',help_text='You can cutomize the ADA Widget color. For example: #FF5733')
    
    aioa_place = models.CharField(max_length=100,blank=True,choices=aioa_SELECT_CHOICE,default=('bottom_right','Bottom Right'),verbose_name='Where would you like to place the accessibility icon on your site')
    
    aioa_icon_type = RadioGridField(rows=ROWS, values=CHOICES,require_all_fields = False,default=('aioa-icon-type-1',format_html('<img  src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />')),verbose_name='Icon Type')
    
    aioa_icon_size = RadioGridField(rows=ROWS,values=CHOICES1,require_all_fields = False,default=('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), verbose_name='Icon Size',help_text=icon_change)
    
    # aioa_icon_mobile = RadioGridField(rows=ROWS, values=CHOICES1,default=('aioa-default-icon', format_html('<img class="csticontype" src="https://skynettechnologies.com/sites/default/files/python/{}" width="55" height="55" />',value_i)), require_all_fields=True,verbose_name='Icon Size For Mobile',help_text=icon_change)

    def __str__(self):
        return '{}'.format("All in One Accessibility Settings")

    class Meta:
        verbose_name = 'All in One Accessibility Settings'
        verbose_name_plural = 'All in One Accessibility Settings'   

