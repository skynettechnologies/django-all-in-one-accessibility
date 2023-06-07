Django All in One Accessibility
===============================

*Django All in One Accessibility is a django App based on assistive technology that helps organizations enhance the accessibility and usability of their website Detailed documentation is in the "docs" directory.


Quick start
============

- ``settings.py`` — add 'accessibility' in your INSTALLED_APPS

- ``settings.TEMPLATES`` — put this line in TEMPLATES context_processors to `accessibility.context_processors.admin_AIOA`

- ``base.html`` — put this line in footer of your base. html to `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`

Run ``python manage.py migrate`` to create the  All in One Accessibility models

Start the development server and visit http://127.0.0.1:8000/admin/ to create a All in One Accessibility 