import logging

from django.apps import AppConfig

logger = logging.getLogger("accessibility")


class AccessibilityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accessibility'

    def ready(self):
        """
        Only wires the post_migrate signal that creates the default settings.
        Domain registration is NOT done here: it happens when an admin opens
        the settings page (see registration.register_current_domain), the same
        way the Odoo module does it.
        """
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_default_settings, sender=self)


def _create_default_settings(sender, **kwargs):
    """
    Creates the default AllinOneAccessibility settings record after migrations
    if one does not already exist. This ensures the settings page is pre-populated
    with sensible defaults (bottom_right position, oversize widget, etc.) the
    moment the module is installed — no manual save required.
    """
    try:
        from .models import AllinOneAccessibility
        if not AllinOneAccessibility.objects.exists():
            AllinOneAccessibility.objects.create()
            logger.info("[AIOA] Default accessibility settings created.")
    except Exception as e:
        # Table may not exist yet on the very first migrate run before
        # the migration has been applied — safe to ignore.
        logger.warning("[AIOA] Could not create default settings: %s", e)
