def admin_AIOA(request):
    """
    Injects the correct AIOA widget JS URL (EU or non-EU) into templates.
    The EU flag is the one recorded when the domain was registered
    (AioaDomainRegistration.no_required_eu); defaults to the non-EU script.
    """
    eu_script_url   = 'https://eu.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?'
    aioa_script_url = 'https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode='

    from .registration import get_no_required_eu
    no_required_eu = get_no_required_eu(request)

    return {'AIOA_URL': eu_script_url if no_required_eu == 0 else aioa_script_url}
