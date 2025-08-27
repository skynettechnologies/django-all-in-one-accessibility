# Create your models here.

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# Cleaned up and corrected choices
AIOA_SELECT_CHOICES = [
    ('top_left', 'Top Left'),
    ('top_center', 'Top Center'),
    ('top_right', 'Top Right'),
    ('middle_left', 'Middle Left'),
    ('middle_center', 'Middle Center'),
    ('middle_right', 'Middle Right'),
    ('bottom_left', 'Bottom Left'),
    ('bottom_right', 'Bottom Right'),
]

AIOA_SIZE_CHOICES = [
    ('regular', 'Regular Size'),
    ('oversize', 'Oversize'),
]

AIOA_ICON_TYPE_CHOICES = [
    ('aioa-icon-type-1', ''),
    ('aioa-icon-type-2', ''),
    ('aioa-icon-type-3', ''),
    ('aioa-icon-type-4', ''),
    ('aioa-icon-type-5', ''),
    ('aioa-icon-type-6', ''),
    ('aioa-icon-type-7', ''),
    ('aioa-icon-type-8', ''),
    ('aioa-icon-type-9', ''),
    ('aioa-icon-type-10', ''),
    ('aioa-icon-type-11', ''),
    ('aioa-icon-type-12', ''),
    ('aioa-icon-type-13', ''),
    ('aioa-icon-type-14', ''),
    ('aioa-icon-type-15', ''),
    ('aioa-icon-type-16', ''),
    ('aioa-icon-type-17', ''),
    ('aioa-icon-type-18', ''),
    ('aioa-icon-type-19', ''),
    ('aioa-icon-type-20', ''),
    ('aioa-icon-type-21', ''),
    ('aioa-icon-type-22', ''),
    ('aioa-icon-type-23', ''),
    ('aioa-icon-type-24', ''),
    ('aioa-icon-type-25', ''),
    ('aioa-icon-type-26', ''),
    ('aioa-icon-type-27', ''),
    ('aioa-icon-type-28', ''),
    ('aioa-icon-type-29', ''),
]

to_the_right_choice = [('to_the_left','To the left'),
      ('to_the_right','To the right'),
    ]

to_the_bottom_choice = [('to_the_bottom','Top the bottom'),
      ('to_the_top','To the top'),
    ]

AIOA_ICON_SIZE_CHOICES = [
    ('aioa-big-icon', ''),
    ('aioa-medium-icon', ''),
    ('aioa-default-icon', ''),
    ('aioa-small-icon', ''),
    ('aioa-extra-small-icon', ''),
]


class AllInOneAccessibility(models.Model):
   
    aioa_color_code = models.CharField(
        max_length=50,
        blank=True,
        default='',
        verbose_name='Hex Color Code',
        help_text='You can customize the ADA Widget color. For example: #FF5733'
    )

    enable_widget_icon_position = models.BooleanField(
        default=False,
        verbose_name="Enable Precise accessibility widget icon position"
    )

    to_the_right_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Right offset (PX)",
        help_text="0 - 250px are permitted values"
    )

    to_the_right = models.CharField(
        default='to_the_left',choices=to_the_right_choice,
        verbose_name="To the left"
    )

    to_the_bottom_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Bottom offset (PX)",
        help_text="0 - 250px are permitted values"
    )

    to_the_bottom = models.CharField(
        default='to_the_bottom',choices=to_the_bottom_choice,
        verbose_name="To the bottom"
    )
    
    aioa_place = models.CharField(
        max_length=100,
        choices=AIOA_SELECT_CHOICES,
        default='bottom_right',
        verbose_name='Where would you like to place the accessibility icon on your site'
    )

    aioa_size = models.CharField(
        max_length=20,
        choices=AIOA_SIZE_CHOICES,
        default='oversize',
        verbose_name='Select Widget Size'
    )
    
    aioa_icon_type = models.CharField(
        max_length=50,
        choices=AIOA_ICON_TYPE_CHOICES,
        default='aioa-icon-type-1',
        verbose_name='Icon Type'
    )

    enable_icon_custom_size = models.BooleanField(
        default=False,
        verbose_name="Enable Icon Custom Size"
    )

    aioa_size_value = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        verbose_name="Select exact icon size (PX)",
        help_text="20 - 150px are permitted values"
    )

    
    aioa_icon_size = models.CharField(
        max_length=50,
        choices=AIOA_ICON_SIZE_CHOICES,
        default='aioa-default-icon',
        verbose_name='Icon Size',
        help_text='This size preview will change according to the selected icon type.'
    )
        
    def __str__(self):
        return 'All in One Accessibility Settings'

    class Meta:
        verbose_name = 'All in One Accessibility Settings'
        verbose_name_plural = 'All in One Accessibility Settings'
       
 


