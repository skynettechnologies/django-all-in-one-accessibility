"""
registration.py
---------------
Domain registration with Skynet's add-user-domain API.

Modelled on the Odoo module (aioa_register_domain.js). There is NO
registration at startup / install / migrate, no background thread, and no
looping over ALLOWED_HOSTS. A domain is registered only when a staff user
opens the "All in One Accessibility" settings page in the Django admin, and
only for the one domain that admin session is on:

  * hostname is taken from the request (Django has already validated it
    against ALLOWED_HOSTS), or from settings.AIOA_DOMAIN when you set it
    explicitly (useful behind proxies / internal hostnames)
  * localhost / 127.0.0.1 / 0.0.0.0 are never registered
  * add-user-domain is called ONE time only per domain (MAX_REGISTER_ATTEMPTS
    = 1), whether Skynet answers 200 or fails. The attempt is recorded before
    the call, so no later page open, restart or worker can call it again.
    (To allow one new attempt, delete that domain's AioaDomainRegistration
    row, e.g. from `manage.py shell`.)
  * the attempt is "claimed" with an atomic UPDATE before the HTTP call, so
    two admins (or two workers) opening the page at once cannot both call
    the API
  * state lives in the AioaDomainRegistration table, so it survives
    restarts, redeploys and read-only / ephemeral filesystems
"""

import base64
import logging
from datetime import timedelta, datetime
from urllib.parse import urlparse

import requests

logger = logging.getLogger("accessibility")

ADD_USER_DOMAIN_URL = "https://ada.skynettechnologies.us/api/add-user-domain"
WIDGET_SETTINGS_URL = "https://ada.skynettechnologies.us/api/widget-settings"
MAX_REGISTER_ATTEMPTS = 1  # add-user-domain is called ONE time only, ever
# An attempt that started less than this many seconds ago is considered still
# in flight; nobody else may start another one for the same domain.
_IN_FLIGHT_SECONDS = 30
LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0"}

# Default python-requests User-Agent gets throttled (429) by the Skynet API's
# WAF/rate-limiter. Sending a normal, identifiable UA avoids that.
_REQUEST_HEADERS = {
    "User-Agent": "AIOA-Django-Plugin/3.0.5 (+https://ada.skynettechnologies.us)",
    "Accept": "*/*",
}


def get_canonical_domain(request):
    """
    Returns (domain_url, hostname) exactly as Skynet keys a site:
    "https://" + hostname, no port, always https.
    Used for BOTH registration and the settings sync so they always match.
    """
    from django.conf import settings

    raw = getattr(settings, "AIOA_DOMAIN", None)
    if raw:
        raw = raw.strip().rstrip("/")
        hostname = urlparse(raw).hostname if "://" in raw else raw.split(":")[0]
    else:
        hostname = urlparse(request.build_absolute_uri()).hostname
    return f"https://{hostname}", hostname


def _detect_eu():
    """Returns True if the server is in an EU country."""
    try:
        resp = requests.get("https://ipapi.co/json/", headers=_REQUEST_HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("in_eu", False)
    except Exception:
        pass
    return False


def _say(message):
    """Log the outcome of a registration attempt."""
    logger.info(message)


def register_current_domain(request):
    """
    Registers the domain of the current admin request if it is not yet
    registered. Safe to call on every settings page open: it returns at once
    when there is nothing to do. Never raises. Every outcome (called or
    skipped, and why) is printed to the server console.
    """
    try:
        _register_current_domain(request)
    except Exception as e:  # registration must never break the admin page
        hint = ""
        if "no such table" in str(e) or "does not exist" in str(e) or "doesn't exist" in str(e):
            hint = " -> the database table is missing: run `python manage.py migrate`"
        _say(f"[AIOA] add-user-domain NOT called, error: {e}{hint}")


def _register_current_domain(request):
    from django.db.models import F, Q
    from django.utils import timezone
    from .models import AioaDomainRegistration

    domain_url, hostname = get_canonical_domain(request)

    reset_cmd = f"delete the AioaDomainRegistration row for '{hostname}' (e.g. from `manage.py shell`)"

    if not hostname or hostname in LOCAL_HOSTS:
        _say(
            f"[AIOA] add-user-domain NOT called: '{hostname}' is a local host. "
            "Open the admin using your real domain (e.g. http://yourdomain.com:8000/admin/)."
        )
        return  # dev/local instance - nothing to register

    row, _ = AioaDomainRegistration.objects.get_or_create(domain=hostname)
    if row.registered:
        _say(
            f"[AIOA] add-user-domain NOT called for {hostname}: already registered "
            f"(HTTP {row.last_status_code} on {row.registered_at}). It is only ever called once. "
            f"If this site is missing on the Skynet dashboard, {reset_cmd}"
        )
        return
    if row.attempts >= MAX_REGISTER_ATTEMPTS:
        _say(
            f"[AIOA] add-user-domain NOT called for {hostname}: its one attempt was already used "
            f"(HTTP {row.last_status_code} on {row.last_attempt_at}). To try again, {reset_cmd}"
        )
        return

    # Atomically claim this attempt. Exactly one concurrent caller gets
    # updated == 1; everyone else sees 0 and backs off.
    now = timezone.now()
    in_flight_cutoff = now - timedelta(seconds=_IN_FLIGHT_SECONDS)
    claimed = AioaDomainRegistration.objects.filter(
        pk=row.pk,
        registered=False,
        attempts__lt=MAX_REGISTER_ATTEMPTS,
    ).filter(
        Q(last_attempt_at__isnull=True) | Q(last_attempt_at__lt=in_flight_cutoff)
    ).update(attempts=F("attempts") + 1, last_attempt_at=now)
    if claimed != 1:
        _say(f"[AIOA] add-user-domain NOT called for {hostname}: another request is registering it right now.")
        return

    no_required_eu = 0 if _detect_eu() else 1

    payload = {
        "name":            hostname,
        "email":           f"no-reply@{hostname}",
        "company_name":    "",
        "website":         base64.b64encode(domain_url.encode()).decode(),
        "package_type":    "basic",
        "start_date":      datetime.utcnow().isoformat(),
        "end_date":        "",
        "price":           "",
        "discount_price":  "0",
        "platform":        "Django",
        "api_key":         "",
        "is_trial_period": "",
        "is_free_widget":  "1",
        "bill_address":    "",
        "country":         "",
        "state":           "",
        "city":            "",
        "post_code":       "",
        "transaction_id":  "",
        "subscr_id":       "",
        "payment_source":  "",
        "no_required_eu":  no_required_eu,
    }

    status = None
    body = ""
    _say(f"[AIOA] Calling add-user-domain for {hostname} ...")
    try:
        response = requests.post(
            ADD_USER_DOMAIN_URL, data=payload, headers=_REQUEST_HEADERS, timeout=10
        )
        status = response.status_code
        body = (response.text or "")[:300]
    except Exception as e:
        body = str(e)
        logger.warning("[AIOA] add-user-domain call failed for %s: %s", hostname, e)

    if status == 200:
        AioaDomainRegistration.objects.filter(pk=row.pk).update(
            registered=True,
            registered_at=timezone.now(),
            no_required_eu=no_required_eu,
            last_status_code=200,
        )
        _say(f"[AIOA] \u2713 add-user-domain HTTP 200 for {hostname}. Response: {body}")
    else:
        AioaDomainRegistration.objects.filter(pk=row.pk).update(last_status_code=status)
        _say(
            f"[AIOA] \u2717 add-user-domain FAILED for {hostname}: HTTP {status}. Response: {body} "
            f"(not retried automatically; to try again, {reset_cmd})"
        )


def get_no_required_eu(request):
    """
    1 = non-EU script, 0 = EU script. Read from the registration row of this
    request's domain, else any registered row, else non-EU default.
    """
    try:
        from .models import AioaDomainRegistration
        _, hostname = get_canonical_domain(request)
        row = (
            AioaDomainRegistration.objects.filter(domain=hostname, registered=True).first()
            or AioaDomainRegistration.objects.filter(registered=True).first()
        )
        if row is not None:
            return row.no_required_eu
    except Exception:
        pass
    return 1
