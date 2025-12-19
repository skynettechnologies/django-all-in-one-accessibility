# Context processor to inject the AIOA widget base script URL into templates
import os
import json

def admin_AIOA(request):
    """
    Context processor to inject the correct AIOA or EU widget JS URL
    depending on the 'no_required_eu' value from the one-time API call.
    """
    eu_script_url = 'https://eu.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?'
    aioa_script_url = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='

    # Default script if flag file is missing
    script_to_use = aioa_script_url

    # Path to the one-time API call flag file
    FLAG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".accessibility_api_called.json")

    if os.path.exists(FLAG_FILE):
        try:
            with open(FLAG_FILE, "r") as f:
                data = json.load(f)
                # Use no_required_eu if present, fallback to in_eu
                no_required_eu = data.get("no_required_eu", 1 if not data.get("in_eu", False) else 0)
                
                # Determine which script to inject
                if no_required_eu == 0:
                    script_to_use = eu_script_url
                elif no_required_eu == 1:
                    script_to_use = aioa_script_url

        except Exception as e:
            error_content = str(e)
    return {'AIOA_URL': script_to_use}
