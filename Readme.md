# All in One Accessibility
All in One Accessibility AI free Widget Supports limited 23 features only and includes 140 Languages.

It improves website ADA compliance and browser experience for ADA, WCAG 2.0, 2.1 & 2.2, Section 508, California Unruh Act, Australian DDA, European EAA EN 301 549, UK Equality Act (EA), Israeli Standard 5568, Ontario AODA, Canada ACA, German BITV, France RGAA, Brazilian Inclusion Law (LBI 13.146/2015), Spain UNE 139803:2012, JIS X 8341 (Japan), Italian Stanca Act and Switzerland DDA Standards.

Follows the best industry security, SEO practices and standards ISO 9001:2015 & ISO 27001:2013 and complies with GDPR, COPPA regulations. Member of W3C and International Association of Accessibility Professionals (IAAP). It is a flexible & lightweight widget that can be changed according to law and reduces the risk of time-consuming accessibility lawsuits.

For more details/features, Please visit [All in One Accessibility](https://www.skynettechnologies.com/all-in-one-accessibility)

Unlock over 70 features with the All in One Accessibility Widget through a paid subscription. See the detailed comparison of Paid vs. Free features [here](https://www.skynettechnologies.com/all-in-one-accessibility/features).

We provide a 10-day free trial. Get started [here](https://ada.skynettechnologies.us/trial-subscription?utm_source=all-in-one-accessibility&utm_medium=landing-page&utm_campaign=trial-subscription).

#### You can use this package in Django/Django-CMS/Django-Oscar
---

## Installation
-   Run `pip install django-all-in-one-accessibility`
-   Add `accessibility` in `settings.INSTALLED_APPS`
-   Add `accessibility.context_processors.admin_AIOA` in `settings.TEMPLATES context_processors`
-   Add `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`put this line in your base.html footer
-   Run `python manage.py migrate`
-   Run `python manage.py runserver` for Restart your application server

---

## Usage


## Steps for Django and Django CMS
---

### Settings.INSTALLED_APPS
Just add `accessibility` in to your setting.INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accessibility',
]
```

### Settings.TEMPLATES
Just add `accessibility.context_processors.admin_AIOA` in your setting.TEMPLATES:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'accessibility.context_processors.admin_AIOA',
            ],
        },
    },
]
```

### Base.html
Just add this tag in your base.html footer(your main template of django website) `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`:
```python
  <footer>
    <script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>
  </footer>
```

### Migrate
Migrate your app
```python
python manage.py migrate

```

### Restart
Restart your app server with this command and check the admin panel the model is ready to use
```python
python manage.py runserver
```
---
## Steps for Django Oscar
---
### Settings.INSTALLED_APPS
Just add `accessibility` in to your setting.INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accessibility',
]
```

### Settings.TEMPLATES
Just add `accessibility.context_processors.admin_AIOA` in your setting.TEMPLATES:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'accessibility.context_processors.admin_AIOA',
            ],
        },
    },
]
```

### Base.html
There is some changes in base.html file for Oscar project `when u are using django oscar there is already base.html file exists so u need to go to oscar project directory which are locate in your site-packages(go to site-packages -> oscar -> templates ->oscar -> base.html) put this tag <script id="aioa-adawidget" src="{{ AIOA_URL }}"></script> in oscar/templates/oscar/base.html footer`
```python
<footer>
	<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>
</footer>
```

### Migrate
Migrate your app
```python
python manage.py migrate

```

### Restart
Restart your app server with this command and check the admin panel the model is ready to use
```python
python manage.py runserver
```
## Screenshots

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-1.jpg?v=2)

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-2.jpg?v=2)

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-3.jpg?v=2)

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-4.jpg?v=2)

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-5.jpg?v=2)

![App Screenshot](https://www.skynettechnologies.com/sites/default/files/Screenshot-6.jpg?v=2)

## Video

[![All in One Accessibility](https://img.youtube.com/vi/I-DjgZyleeI/0.jpg)](https://www.youtube.com/watch?v=I-DjgZyleeI)

## Documentation

- [Purchase Django All in One Accessibility](https://www.skynettechnologies.com/django-website-accessibility)
- [How to install All in One Accessibility Addon on Django](https://www.skynettechnologies.com/blog/django-cms-web-accessibility-widget-installation)
- [All in One Accessibility - Features Guide](https://www.skynettechnologies.com/sites/default/files/accessibility-widget-features-list.pdf)

## Submit a Support Request

Please visit our [support page](https://www.skynettechnologies.com/report-accessibility-problem) and fill out the form. Our team will get back to you as soon as possible.

## Send Us an Email

Alternatively, you can send an email to our support team:
[hello@skynettechnologies.com](mailto:hello@skynettechnologies.com)

## Partnership Opportunities

#### [Agency Partnership](https://www.skynettechnologies.com/agency-partners)

Partner with us as an agency to provide comprehensive accessibility solutions to your clients. Get access to exclusive resources, training, and support to help you implement and manage accessibility features effectively.

#### [Affiliate Partnership](https://www.skynettechnologies.com/affiliate-partner)

Join our affiliate program and earn commissions by promoting All in One Accessibility™. Share our Widget with your network and help businesses improve their website accessibility while generating revenue.

For more details, Please visit [Partnership Opportunities Page](https://www.skynettechnologies.com/partner-program)

## Credits

This addon is developed and maintained by [Skynet Technologies USA LLC](https://www.skynettechnologies.com)

## Current Maintainers
- [Skynet Technologies USA LLC](https://github.com/skynettechnologies)
