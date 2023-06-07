=====
Django All in One Accessibility
=====

Django All in One Accessibility is a django App based on assistive technology that helps organizations enhance the accessibility and usability of their website Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "accessibility" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "accessibility",
    ]

2. accessibility.context_processors.admin_AIOA (add this line in settings.TEMPLATES context_processors)


3.  put this line in your base.html(your main template)footer <script id="aioa-adawidget" src="{{ AIOA_URL }}"> </script>
    Note: The Django template system provides you with template inheritance that allows you to extend base HTML file across your Django templates you can extend it in other template files using the syntax {% extends 'base.html' %}
    for example:

4. Run ``python manage.py migrate`` to create the  All in One Accessibility models. 

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a All in One Accessibility 

