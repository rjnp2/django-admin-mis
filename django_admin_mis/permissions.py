from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class CustomStaffPermission(DjangoModelPermissions):
    perms_map = {
        'GET': 'has_view_permission',
        'OPTIONS': 'has_view_permission',
        'HEAD': 'has_view_permission',
        'POST': 'has_add_permission',
        'PUT': 'has_change_permission',
        'PATCH': 'has_change_permission',
        'DELETE': 'has_delete_permission',
    }
    
    def has_permission(self, request, view):
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and 
           self.authenticated_users_only and 
           not request.user.is_staff):
            return False
        
        if request.method not in self.perms_map:
            raise exceptions.MethodNotAllowed(request.method)
        
        app_name = view.kwargs.get('app_name')
        model_name = view.kwargs.get('model_name')
        
        if not (app_name and model_name):
            return True
        
        _, register_app = view.get_model_register_admin()
        
        map_method = self.perms_map[request.method]
        
        return getattr(register_app, map_method)(request)
    
    def has_object_permission(self, request, view, obj):
        _, register_app = view.get_model_register_admin()
        map_method = self.perms_map[request.method]
        permis = getattr(register_app, map_method)
        
        if request.method == 'POST':
            return permis(request)
        return (request, obj)
    