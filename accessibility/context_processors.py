import os
import json

def admin_AIOA(request):
    """
    Injects the correct AIOA widget JS URL (EU or non-EU) into templates.
    Reads no_required_eu from the new per-domain flag file format.
    """
    eu_script_url   = 'https://eu.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?'
    aioa_script_url = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='
    script_to_use   = aioa_script_url  # safe default

    FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")

    if os.path.exists(FLAG_FILE):
        try:
            with open(FLAG_FILE, "r") as f:
                data = json.load(f)

            # ── New format: {"domains": {"example.com": {"no_required_eu": 1}}} ──
            no_required_eu = 1  # default non-EU
            domains = data.get("domains", {})
            if domains:
                # Use the first registered domain's EU flag
                first = next(iter(domains.values()))
                no_required_eu = first.get("no_required_eu", 1)
            else:
                # ── Old single-domain format (upgrade path) ──
                no_required_eu = data.get("no_required_eu", 1 if not data.get("in_eu", False) else 0)

            script_to_use = eu_script_url if no_required_eu == 0 else aioa_script_url

        except Exception:
            pass  # fall back to default non-EU script

    return {'AIOA_URL': script_to_use}
