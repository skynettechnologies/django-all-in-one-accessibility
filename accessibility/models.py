# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Model to store accessibility settings
AIOA_SELECT_CHOICES = [
    ('top_left', 'Top Left'),
    ('top_center', 'Top Center'),
    ('top_right', 'Top Right'),
    ('middle_left', 'Middle Left'),
    ('middle_right', 'Middle Right'),
    ('bottom_left', 'Bottom Left'),
    ('bottom_center', 'Bottom Center'),
    ('bottom_right', 'Bottom Right'),
]

AIOA_SIZE_CHOICES = [
    ('regular', 'Regular Size'),
    ('oversize', 'Oversize'),
]

TO_THE_RIGHT_CHOICES = [
    ('to_the_left', 'To the left'),
    ('to_the_right', 'To the right'),
]

TO_THE_BOTTOM_CHOICES = [
    ('to_the_bottom', 'To the bottom'),
    ('to_the_top', 'To the top'),
]

AIOA_ICON_SIZE_CHOICES = [
    ('aioa-big-icon', 'Big'),
    ('aioa-medium-icon', 'Medium'),
    ('aioa-default-icon', 'Default'),
    ('aioa-small-icon', 'Small'),
    ('aioa-extra-small-icon', 'Extra Small'),
]

ICON_CHOICES = [
    (f'aioa-icon-type-{i}', f'https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-{i}.svg')
    for i in range(1, 30)
]

  
class AllinOneAccessibility(models.Model):
    aioa_color_code = models.CharField(
        max_length=50,
        blank=True,
        default='420083',
        verbose_name='Hex Color Code',
        help_text='Customize the ADA Widget color. Example: #FF5733'
    )

    enable_widget_icon_position = models.BooleanField(
        default=False,
        verbose_name="Enable Precise widget icon positioning"
    )

    to_the_right_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Right offset (PX)",
        help_text="0 - 250px are permitted values"
    )

    to_the_right = models.CharField(
        max_length=50,
        default='to_the_left',
        choices=TO_THE_RIGHT_CHOICES,
        verbose_name="To the right"
    )

    to_the_bottom_px = models.PositiveSmallIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(250)],
        verbose_name="Bottom offset (PX)",
        help_text="0 - 250px are permitted values"
    )

    to_the_bottom = models.CharField(
        max_length=50,
        default='to_the_bottom',
        choices=TO_THE_BOTTOM_CHOICES,
        verbose_name="To the bottom"
    )

    aioa_place = models.CharField(
        max_length=100,
        choices=AIOA_SELECT_CHOICES,
        default='bottom_right',
        verbose_name='Position of the accessibility icon'
    )

    aioa_size = models.CharField(
        max_length=20,
        choices=AIOA_SIZE_CHOICES,
        default='oversize',
        verbose_name='Widget Size'
    )

    aioa_icon_type = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='aioa-icon-type-1',
        verbose_name='Icon Type'
    )

    enable_icon_custom_size = models.BooleanField(
        default=False,
        verbose_name="Enable Custom Icon Size"
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
        verbose_name='Desktop Icon Size',
    )
    
    def __str__(self):
        return "All in One Accessibility"
    
    class Meta:
        verbose_name = "All in One Accessibility"
        verbose_name_plural = "All in One Accessibility"



class AioaDomainRegistration(models.Model):
    """
    One row per domain registered with Skynet's add-user-domain API.
    Registration happens only when an admin opens the settings page (see
    registration.py); this table is the single source of truth for "already
    registered", the attempt count and the last API status, so duplicate
    registrations can be audited and prevented.
    """
    domain = models.CharField(max_length=255, unique=True)
    registered = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    no_required_eu = models.PositiveSmallIntegerField(default=1)
    last_status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = "AIOA domain registration"
        verbose_name_plural = "AIOA domain registrations"
