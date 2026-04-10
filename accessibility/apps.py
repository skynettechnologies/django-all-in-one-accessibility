from django.apps import AppConfig


class AccessibilityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accessibility'

    def ready(self):
        """
        Fires on every Django startup — runserver, migrate, gunicorn, uwsgi.
        Runs registration in a background thread so startup is never blocked.
        Flag file ensures add-user-domain is called only once per domain,
        regardless of how many times Django starts up.
        Connects post_migrate signal to create default settings on first install.
        """
        import threading
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_default_settings, sender=self)

        threading.Thread(
            target=_run_registration,
            daemon=False,  # must complete — not killed on process exit
        ).start()


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
            print("[AIOA] ✓ Default accessibility settings created.")
    except Exception as e:
        # Table may not exist yet on the very first migrate run before
        # the migration has been applied — safe to ignore.
        print(f"[AIOA] Could not create default settings: {e}")


def _run_registration():
    """Background thread target — safe wrapper around registration."""
    try:
        from .registration import register_domain_on_install
        register_domain_on_install()
    except Exception as e:
        print(f"[AIOA] Registration error: {e}")
