from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class CustomStaffPermission(DjangoModelPermissions):
    # Define a mapping of HTTP methods to corresponding permission check methods
    method_to_permission_map = {
        'GET': 'has_view_permission',
        'OPTIONS': 'has_view_permission',
        'HEAD': 'has_view_permission',
        'POST': 'has_add_permission',
        'PUT': 'has_change_permission',
        'PATCH': 'has_change_permission',
        'DELETE': 'has_delete_permission',
    }

    def has_permission(self, request, view):
        # Check if the view has requested to ignore model permissions
        if getattr(view, '_ignore_model_permissions', False):
            return True

        # Check if the request user is authenticated and is a staff member
        if not request.user or (
            not request.user.is_authenticated and
            self.authenticated_users_only and
            not request.user.is_staff
        ):
            return False

        # Ensure that the HTTP method is supported by our permissions
        if request.method not in self.method_to_permission_map:
            raise exceptions.MethodNotAllowed(request.method)

        # Extract the 'app_name' and 'model_name' from view's kwargs
        app_name = view.kwargs.get('app_name')
        model_name = view.kwargs.get('model_name')

        # If 'app_name' or 'model_name' is not provided, allow access
        if not (app_name and model_name):
            return True

        # Get the register_app associated with the view's model
        _, register_app = view.get_model_register_admin()

        # Determine the permission check method based on the HTTP method
        permission_check_method = self.method_to_permission_map[request.method]

        # Call the appropriate permission check method on the register_app
        return getattr(register_app, permission_check_method)(request)

    def has_object_permission(self, request, view, obj):
        # Get the register_app associated with the view's model
        _, register_app = view.get_model_register_admin()

        # Determine the permission check method based on the HTTP method
        permission_check_method = self.method_to_permission_map[request.method]

        # Get the permission check function from the register_app
        permission_check_function = getattr(register_app, permission_check_method)

        # Call the permission check function for the given object
        if request.method == 'POST':
            return permission_check_function(request)
        else:
            return permission_check_function(request, obj)
