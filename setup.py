from setuptools import setup,find_packages
if __name__ == "__main__":
    setup(

        name = "django-all-in-one-accessibility",
        version = "3.0.0",
        author='Skynet Technologies USA LLC',
        author_email='developer3@skynettechnologies.com',
        description = "All in One Accessibility widget makes it easy for users to customize their experience in a single click tap or press of a button",
        readme = "Readme.md",
        packages=find_packages(),
        install_requires = [
            "Django>=4.1,<5.3",
            "requests>=2.25.0",
        ],
        classifiers = [
            "Programming Language :: Python :: 3",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Framework :: Django :: 5.2",
            "Framework :: Django :: 5.1",
            "Framework :: Django :: 5.0",
            "Framework :: Django :: 4.2",
            "Framework :: Django :: 4.1",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.13",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        ],

        include_package_data = True,
                
    )


