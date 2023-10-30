import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-admin-mis', 
    version='0.0.1',
    packages=['django_admin_mis'],
    include_package_data=True,
    license='MIT License',
    description='django-admin-mis is a Django application designed to simplify the management of Single Sign-On (SSO) clients within a web application. It provides functionalities for handling login and logout processes and conveniently sets codes in cookies for seamless authentication and user session management. By integrating this app into a Django project, developers can streamline the implementation of SSO functionality and enhance the overall user experience.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/rjnp2/django-admin-mis',
    author='rjnp2',
    author_email='rjnp2@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.8",
    install_requires=[
        'requests>=2.28.1',
    ],
    extras_require={
        "dev": ['twine>=4.0.2',]
    }
)
