"""
registration.py
---------------
Registers ALL valid domains from ALLOWED_HOSTS with add-user-domain API.
Each domain tracked independently. New domains register on next migrate.
"""

import os
import json
import base64
import requests
from datetime import datetime

# Default python-requests User-Agent gets throttled (429) by the Skynet API's
# WAF/rate-limiter. Sending a normal, identifiable UA avoids that.
_REQUEST_HEADERS = {
    "User-Agent": "AIOA-Django-Plugin/3.0.3 (+https://ada.skynettechnologies.us)",
    "Accept": "*/*",
}


def _get_flag_file():
    """
    Returns the flag file path.
    Priority:
      1. BASE_DIR/accessibility_registered.json  (project root — writable everywhere)
      2. Fallback to package dir (venv installs)
    """
    try:
        from django.conf import settings
        if hasattr(settings, 'BASE_DIR'):
            return os.path.join(str(settings.BASE_DIR), ".aioa_registered.json")
    except Exception:
        pass
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")


def _is_valid_registration(info):
    """
    A domain is only genuinely registered if the recorded response was an
    actual HTTP 200 — mirrors the guard in the Shopyo plugin's
    _register_domain(), which never persists a non-200 result at all.

    Older versions of this plugin could persist a domain with
    api_called: True even when status_code was 429 (or another non-200),
    which permanently blocked any retry — the domain looked "done" forever
    even though add-user-domain never actually succeeded for it. Treat any
    entry that isn't a clean 200 as unregistered so it gets retried and the
    flag file self-heals instead of requiring a manual edit.
    """
    return isinstance(info, dict) and info.get("api_called") is True and info.get("status_code") == 200


def _read_flag():
    """
    Returns dict of already-registered domains: {domain_name: info}.
    Filters out any stale/corrupted entries that aren't a genuine HTTP 200
    registration (see _is_valid_registration) so they're retried instead
    of staying stuck forever.
    """
    flag_file = _get_flag_file()
    raw = {}

    if not os.path.exists(flag_file):
        # Also check legacy package-dir location for upgrades
        legacy = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")
        if os.path.exists(legacy):
            try:
                with open(legacy, "r") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "domain" in data and "domains" not in data:
                    raw = {data["domain"]: data}
                else:
                    raw = data.get("domains", {})
            except Exception:
                raw = {}
    else:
        try:
            with open(flag_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict) and "domain" in data and "domains" not in data:
                raw = {data["domain"]: data}
            else:
                raw = data.get("domains", {})
        except Exception:
            raw = {}

    cleaned = {name: info for name, info in raw.items() if _is_valid_registration(info)}

    dropped = set(raw) - set(cleaned)
    if dropped:
        # Persist the repair immediately so the corrupted entries don't
        # keep coming back on every subsequent read.
        print(f"[AIOA] Dropping stale/invalid registration entries for retry: {sorted(dropped)}")
        _write_flag(cleaned)

    return cleaned


def _write_flag(domains):
    """Persist the full domains registry."""
    flag_file = _get_flag_file()
    with open(flag_file, "w") as f:
        json.dump({"domains": domains}, f, indent=2)


def register_domain_on_install():
    """
    Called from post_migrate signal (apps.py).
    Loops over ALL valid domains in ALLOWED_HOSTS.
    - Already registered → skipped
    - New domain, success (HTTP 200) → marks as registered
    - New domain, failure (429 / other non-200 / network error) → NOT marked,
      so it will be retried automatically on the next migrate/restart
    """
    all_domains = _get_all_domains_from_settings()

    if not all_domains:
        return  # No valid domains — silent skip (localhost/dev setup)

    registered = _read_flag()
    changed = False
    in_eu = _detect_eu()
    no_required_eu = 0 if in_eu else 1

    for domain_url, domain_name in all_domains:
        if domain_name in registered:
            continue  # Already registered — skip silently

        try:
            payload = {
                "name":            domain_name,
                "email":           f"no-reply@{domain_name}",
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

            response = requests.post(
                "https://ada.skynettechnologies.us/api/add-user-domain",
                data=payload,
                headers=_REQUEST_HEADERS,
                timeout=10,
            )

            if response.status_code == 200:
                # Only mark as registered on real success.
                registered[domain_name] = {
                    "api_called":     True,
                    "registered_at":  datetime.utcnow().isoformat(),
                    "domain_url":     domain_url,
                    "no_required_eu": no_required_eu,
                    "status_code":    response.status_code,
                }
                changed = True
                print(f"[AIOA] ✓ Registered: {domain_name} (HTTP {response.status_code})")
            else:
                # Non-200 (e.g. 429) — don't mark as registered.
                # Leaving it out of `registered` means it will be retried
                # automatically on the next migrate/restart instead of
                # being silently stuck forever.
                print(
                    f"[AIOA] ✗ Registration failed for {domain_name}: "
                    f"HTTP {response.status_code} — will retry next run"
                )

        except Exception as e:
            # Network-level failure (timeout, DNS, connection error, etc.)
            # Also NOT marked as registered, so it retries next run.
            print(f"[AIOA] ✗ Registration failed for {domain_name}: {e} — will retry next run")

    if changed:
        _write_flag(registered)


def _detect_eu():
    """Returns True if the server is in an EU country."""
    try:
        resp = requests.get("https://ipapi.co/json/", headers=_REQUEST_HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("in_eu", False)
    except Exception:
        pass
    return False


def _get_all_domains_from_settings():
    """
    Returns [(domain_url, domain_name)] for every real host in ALLOWED_HOSTS.
    Skips localhost, 127.0.0.1, wildcards, and duplicates.
    """
    from django.conf import settings

    if hasattr(settings, 'AIOA_DOMAIN'):
        raw = settings.AIOA_DOMAIN.rstrip('/')
        if '://' in raw:
            from urllib.parse import urlparse
            p = urlparse(raw)
            return [(f"{p.scheme}://{p.hostname}", p.hostname)]
        return [(f"https://{raw}", raw)]

    skip = {'localhost', '127.0.0.1', '*', '.localhost', '0.0.0.0'}
    seen = set()
    result = []
    for host in getattr(settings, 'ALLOWED_HOSTS', []):
        clean = host.lstrip('.')
        if clean and clean not in skip and clean not in seen:
            seen.add(clean)
            result.append((f"https://{clean}", clean))
    return result