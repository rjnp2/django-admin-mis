django-admin-mis
=========================

django-admin-mis is a Django application designed to simplify the management of Single Sign-On (SSO) clients within a web application. \
It provides functionalities for handling login and logout processes and conveniently sets codes in cookies for seamless authentication and user session management.\
By integrating this app into a Django project, developers can streamline the implementation of SSO functionality and enhance the overall user experience.

To install the django-admin-mis package and integrate it into your Django project, follow these steps:
------------

1. Use pip to install the package:

    ```python
    pip install django-admin-mis    
    ```

2. Add django_admin_mis to the INSTALLED_APPS list in your project's settings.py file:
    ```python
    INSTALLED_APPS = [
        # other apps
        'django_admin_mis',
    ]  
    ```
        

4. Finally, include the django_admin_mis.urls in your project's urls.py file to set up the necessary URL routes for the SSO functionality:
    ```python
    urlpatterns = [
        # other URL patterns
        path('', include('django_admin_mis.urls')),
    ]  
    ```
    Once you've completed these steps, the django-admin-mis package will be installed, and you'll have integrated its features into your Django project, allowing you to manage SSO clients with login, logout, and code handling functionalities.

Compatibility
-------------
The compatibility information you provided indicates that the django-admin-mis package is compatible with Python 3.8 and Django versions 4 and above.

To ensure proper compatibility, always check the official documentation and release notes of the django-admin-mis package to confirm its support for specific Python and Django versions.
