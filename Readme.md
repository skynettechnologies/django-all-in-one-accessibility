# All in One Accessibility
- All in One Accessibility widget improves django website ADA compliance and browser experience for WCAG 2.1, ATAG 2.0, ADA, Section 508, Australian DDA, European EAA EN 301 549, UK Equality Act (EA), Israeli Standard 5568, and California Unruh standards.
- 2 Minute installation
- Screen Reader, dynamic widget color and position, supports multiple languages (40 languages)
- Reduces the risk of time-consuming accessibility lawsuits.
- Use apps to connect to external services and manage data flows

It uses the accessibility interface which handles UI and design related adjustments. All in One Accessibility app enhances your Django website accessibility to people with hearing or vision impairments, motor impaired, color blind, dyslexia, cognitive & learning impairments, seizure and epileptic, and ADHD problems. It uses the accessibility interface which handles UI and design related adjustments.

[`django-all-in-one-accessibility-introduction`](https://www.youtube.com/watch?v=PPQMWSzroAA) - introduction of All in One Accessibility widget .

---

## Installation
-   Run `pip install django-all-in-one-accessibility==1.2`
-   Add `accessibility` in `settings.INSTALLED_APPS`
-   Add `accessibility.context_processors.admin_AIOA` in `settings.TEMPLATES context_processors`
-   Add `<script id="aioa-adawidget" src="{{ AIOA_URL }}"></script>`put this line in your base.html footer
-   Run `python manage.py migrate`
-   Run `python manage.py runserver` for Restart your application server

---

## Usage

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
Migrate your app Restart your app with this command
```python
python manage.py migrate

```

### Restart 
Restart your app server with this command and check the admin panel the model is ready to use
```python
python manage.py runserver
```


