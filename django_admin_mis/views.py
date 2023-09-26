
from django.apps import apps
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, helpers
from django.contrib.admin.templatetags.admin_list import date_hierarchy
from django.contrib.admin.utils import flatten_fieldsets, get_deleted_objects
from django.db import transaction
from django.db.models import Q
from django.forms.formsets import all_valid
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.response import Response

from .permissions import CustomStaffPermission
from .serializers import (ActionSerializer, AdminMenuSerializer,
                          DynamicSerializer)
from .utils import (get_default_values, level_to_human_readable,
                    python_validator_dict, simple_field_form)


# Create your views here.
class AdminModelViewSet(viewsets.ViewSet,
                        viewsets.GenericViewSet): 
    permission_classes = [CustomStaffPermission, ]
    serializer_class = AdminMenuSerializer
    filter_backends = []
    
    def get_model_register_admin(self):
        app_name = self.kwargs['app_name'].lower()
        model_name = self.kwargs['model_name'].lower()
        
        try:
            model = apps.get_model(app_name, model_name)
        except:
            raise ParseError({'message' : 'Model doesnot exist.'})

        try:
            register_app = admin.site._registry[model]
        except:
            raise ParseError({'message' : 'Admin register doesnot exist.'})
        
        return model, register_app
    
    def get_object(self, register_app):
        pk = self.kwargs['pk']
        try:
            pk = int(pk)
        except:
            raise ParseError({'message' : 'id must be number.'})
        
        instance = register_app.get_object(self.request, pk)
        
        if instance is None:
            raise ParseError({
                "detail": "Not found."
            })
        
        # May raise a permission denied
        self.check_object_permissions(self.request, instance)

        return instance
    
    def get_objects(self, register_app):
        pks = self.kwargs['pk']
        pks = pks.split(',')
        
        instances = []
        for pk in pks:
            try:
                pk = int(pk)
            except:
                raise ParseError({'message' : 'id must be number.'})
        
            instance = register_app.get_object(self.request, pk)
            
            if instance is None:
                raise ParseError({
                    "detail": f"Id {pk} not found."
                })
            
            # May raise a permission denied
            self.check_object_permissions(self.request, instance)
            instances.append(instance)
        return instances
    
    def get_queryset(self):
        return []
    
    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action in ['list', 'action_perform']:
            serializer_class = self.get_serializer_class()
            return serializer_class(*args, **kwargs)
        else:
            model = kwargs.pop('model', None)
            if model is None:
                model, _ = self.get_model_register_admin()

            serializer_class = DynamicSerializer
            return serializer_class(model=model, fields='__all__', *args, **kwargs)
    
    def get_list_display_data(self, data):
        return [
            {
                'id' : dat.id,
                'display' : dat.__str__(),
            } for dat in data
        ]
    
    def get_field_meta(self, request, field, editable, parent_label=None, admin_field=None):
        validators = python_validator_dict(field)
        field_type = simple_field_form(field)
        
        defaults = get_default_values(field)
            
        if field_type in (
            'foreign key', 'many-to-many relationship',
            'one-to-one relationship'
        ):
            if parent_label and parent_label == field.related_model._meta.label:
                data = {
                    'name' : field.name,
                    'verbose_name' : field.verbose_name,
                    'required' : field.blank,
                    'help_text' : field.help_text,
                    "field_type" : field_type,
                    "editable" : False,
                    "inline_parent" : True,
                    'pk_related_name' : field.related_query_name()
                }
                
            else:
                related_model  = field.related_model
                model_name  = related_model._meta.model_name
                app  = related_model._meta.app_label
                api_link  = f"{request.build_absolute_uri('/')}api/v1/admin/{app}/{model_name}/"
                api_link = api_link.replace(' ', '-').replace('_', '-')
                
                query_params = ['filter_list=true', ]
                if admin_field and hasattr(admin_field, 'queryset'):
                    queryset = admin_field.queryset
                    
                    for query in queryset.query.where.children:
                        if not isinstance(query, Q):
                            try:
                                field_name = query.lhs.target.name
                                lookup = query.lookup_name
                                value = query.rhs
                                query_params.append(f'{field_name}__{lookup}={value}')
                            except Exception as e:
                                print(e)
                                
                query_params = '&'.join(query_params)
                api_link += f'?{query_params}'
            
                data = {
                    'name' : field.name,
                    'query' : field._limit_choices_to if hasattr(field, '_limit_choices_to') else None,
                    'verbose_name' : field.verbose_name,
                    'required' : not field.blank,
                    'help_text' : field.help_text,
                    "field_type" : field_type,
                    "editable" : editable,
                    'api_link' : api_link,
                }
        
        else:
            data = {
                'name' : field.name,
                'verbose_name' : field.verbose_name,
                'validators' : validators,
                'required' : not field.blank,
                'help_text' : field.help_text,
                "field_type" : field_type,
                'editable' : editable,
                'defaults' : defaults,
                'choices' : field.flatchoices,
            }
            
            if hasattr(field, 'dim'):
                data['dim'] = field.dim
            
            if hasattr(field, 'srid'):
                data['srid'] = field.srid
            
            if hasattr(field, 'geography'):
                data['geography'] = field.geography
                
            if hasattr(field, '_extent'):
                data['extent'] = field._extent
                
            if hasattr(field, '_tolerance'):
                data['tolerance'] = field._tolerance
            
            if hasattr(field, 'base_field'):
                base_field = field.base_field
                base_validators = python_validator_dict(base_field)
                base_field_type = simple_field_form(base_field)
                
                data['base_data'] = {
                    'validators' : base_validators,
                    'required' : not base_field.blank,
                    'help_text' : base_field.help_text,
                    "field_type" : base_field_type,
                    'editable' : editable,
                    'defaults' : get_default_values(base_field),
                    'choices' : base_field.flatchoices,
                }
                
        return data
                
    def get_fields_meta_data(self, request, fields, admin_fields):
        data = []
        for field in fields:
            
            if field.auto_created:
                if hasattr(field, 'primary_key') and field.primary_key:
                    pass
                else:
                    continue
                
            admin_field = admin_fields.pop(field.name, None)
            editable = not any([not field.editable, admin_field is None, field.primary_key])
            
            result = self.get_field_meta(request, field, editable, admin_field=admin_field)
            data.append(result)
        
        for key, value in admin_fields.items():
            
            validators = python_validator_dict(value)
            
            if hasattr(value, 'max_length'):
                max_length = value.max_length
            elif hasattr(value, 'max_value'):
                max_length = value.max_value
            else:
                max_length = None
                
            data.append({
                'name' : key,
                'verbose_name' : value.label or key,
                'validators' : validators,
                'required' : value.required,
                'help_text' : value.help_text,
                'max_length' : max_length,
                "field_type" : value.widget.input_type if hasattr(value.widget, 'input_type') else 'string',
                'editable' : True,
                'defaults' : None,
                'choices' : value._get_choices() if hasattr(value, '_get_choices') else [],
            })
            
        return data 
    
    def get_inline_fields_meta_data(self, request, fields, parent_label, read_only_data):
        data = []
        for field in fields:
            if field.auto_created:
                if hasattr(field, 'primary_key') and field.primary_key:
                    pass
                else:
                    continue
            
            editable = not any([not field.editable, field.name in read_only_data, field.primary_key])
            result = self.get_field_meta(request, field, editable, parent_label)
            pk_related_name =  result.pop('pk_related_name', None)
            data.append(result)
        return data, pk_related_name
    
    def get_inline_field_data(self, request, final_data, inlines, nest_inline_name=None):
        inline_data = []
        for inline_model in inlines:
        
            read_only_data = inline_model.get_readonly_fields(request)
            parent_label = inline_model.parent_model._meta.label
            
            fields = inline_model.model._meta.get_fields()
            fields, pk_related_name = self.get_inline_fields_meta_data(
                request=request, fields=fields, 
                parent_label=parent_label, read_only_data=read_only_data
            )
            
            if nest_inline_name is None:
                inline_name = inline_model.model._meta.verbose_name.lower().replace(' ', '_')
            else:
                inline_name = nest_inline_name, pk_related_name
                
            data = {
                'fields' : fields,
                'model_name' : inline_model.model._meta.model_name,
                'inline_name' : inline_name,
                
                'app_name' : inline_model.model._meta.app_label,
                'max_num': inline_model.get_max_num(request),
                'min_num': inline_model.get_min_num(request),
                'extra': inline_model.get_extra(request),
                'perms' : {
                    "add": inline_model.has_add_permission(request, None),
                    "change": inline_model.has_change_permission(request, None),
                    "delete": inline_model.has_delete_permission(request, None),
                    "view": inline_model.has_view_permission(request, None),
                }
            }
            
            if hasattr(inline_model, 'get_inline_instances'):
                nested_inlines = inline_model.get_inline_instances(request)
                if nested_inlines:
                    inline_name += '-0-'
                    self.get_inline_field_data(request, data, nested_inlines, inline_name)
                    
            inline_data.append(data)
        
        final_data['inlines'] = inline_data
    
    def get_inline_object_data(self, request, final_data, inline_instances, parent_instance):
        inline_data = []
        for inline_instance in inline_instances:
            kwargs = {inline_instance.get_formset(request, parent_instance).fk.name:parent_instance.id}
            
            inline_model = inline_instance.model
            objects = list(inline_model.objects.filter(**kwargs))
            
            if not objects:
                continue
            
            nested_data = []
            for instance in objects:
                data = {
                    'data' : self.get_serializer(model=inline_model, instance=instance).data,
                    'perms' : {
                        "add": inline_instance.has_add_permission(request, instance),
                        "change": inline_instance.has_change_permission(request, instance),
                        "delete": inline_instance.has_delete_permission(request, instance),
                        "view": inline_instance.has_view_permission(request, instance)
                    },
                'model_name' : inline_model._meta.model_name,
                'app_name' : inline_model._meta.app_label,
                }
                
                if hasattr(inline_instance, 'get_inline_instances'):
                    nest_inlines = inline_instance.get_inline_instances(request, instance)
                    if nest_inlines and instance:
                        self.get_inline_object_data(request, data, nest_inlines, instance)
                    
                nested_data.append(data)
                
            if nested_data:
                inline_data.append(nested_data)
                
        if inline_data:
            final_data['inlines'] = inline_data
    
    def list(self, request, *args, **kwargs):
        app_dict = {
            'admin_meta_data' : {
                'site_header' : admin.site.site_header,
                'site_title' : admin.site.site_title,
                'index_title' : admin.site.index_title,
            }
        }
        for model, model_admin in admin.site._registry.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue
            
            perms = model_admin.get_model_perms(request)
            
            if True not in perms.values():
                continue
            
            info = (app_label, model._meta.model_name)
            model_dict = {
                "verbose_name": model._meta.verbose_name_plural,
                "model_name": model._meta.object_name,
                "perms": perms,
            }
            
            if perms.get("change") or perms.get("view"):
                try:
                    model_dict["api_url"] = reverse(
                        "admin:%s_%s_changelist" % info, current_app=admin.site.name
                    )
                except:
                    pass
                
            if app_label in app_dict:
                app_dict[app_label]["app_models"].append(model_dict)
            else:
                app_dict[app_label] = {
                    "verbose_name": apps.get_app_config(app_label).verbose_name,
                    "app_label": app_label,
                    "app_models": [model_dict],
                }
        
        return Response(app_dict.values())
    
    @action(methods=['GET'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)')
    def list_display_data(self, request, *args, **kwargs):
        _, register_app = self.get_model_register_admin()
        
        all_terms = ['q', 'o', 'p']
        for filter_ in register_app.get_list_filter(request):
            if callable(filter_):
                filter_ = filter_.parameter_name.split('__')[0]
            all_terms.append(filter_.split('__')[0])
        
        if hasattr(request.query_params, '_mutable'):
            request.query_params._mutable = True
        
        filter_list = request.query_params.get('filter_list', None)
        
        [
            request.query_params.pop(key, None)
            for key in list(request.query_params.keys())
            if key.split('__')[0] not in all_terms
        ]
        list_display = register_app.get_list_display(request)
        
        try:
            ch_inst = register_app.get_changelist_instance(request) 
        except Exception as e:
            raise ParseError({
                'message' : f'Error due to {e}'
            })
            
        queryset = ch_inst.result_list
        
        if filter_list == 'true':
            data = self.get_list_display_data(queryset)
            
        else:
            data = []
            for quer in queryset.iterator():
                da = {}
                if 'id' not in list_display:
                    da['id'] = getattr(quer, 'id')
                    
                for i in list_display:
                    
                    if hasattr(register_app, i) and i != '__str__':
                        da[i] = getattr(register_app, i)(quer)
                        
                    else:
                        value = getattr(quer, i)
                        if callable(value):
                            da[i] = value()
                            
                        else:
                            da[i] = str(value) if hasattr(value, 'pk') else value

                data.append(da)
        
        data = {
            'count' : ch_inst.result_count,
            'data_per_page' : ch_inst.list_per_page,
            'data' : data
        }
        
        if ch_inst.date_hierarchy:
            data['date_hierarchy_data'] = date_hierarchy(ch_inst)
            
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/filters')
    def list_filter_data(self, request, *args, **kwargs):
        model, register_app = self.get_model_register_admin()
        
        if hasattr(request.query_params, '_mutable'):
            request.query_params._mutable = True
        
        request.query_params.clear()
        
        data = {}
        ch_inst = register_app.get_changelist_instance(request) 

        absolute_url = request.build_absolute_uri('/')
        if ch_inst.has_filters:
            filter_specs = ch_inst.filter_specs
            filters_list = []
            for filter_data in filter_specs:
                
                if hasattr(filter_data, 'field'):
                    field_type = simple_field_form(filter_data.field)
                else:
                    field_type = None
                
                if field_type and field_type in ('foreign key', 'many-to-many relationship', 'one-to-one relationship'):
                    related_model  = filter_data.field.related_model
                    model_name  = related_model._meta.model_name
                    app  = related_model._meta.app_label
                    admin_url = f"{absolute_url}api/v1/admin/{app}/{model_name}/?filter_list=true"
                    
                    filters_list.append({
                        'title' : filter_data.title,
                        'lookup_kwarg' : filter_data.lookup_kwarg if hasattr(filter_data, 'lookup_kwarg') else None,
                        'field_type' : field_type,
                        'admin_url' : admin_url,
                    })

                else:
                    filters_list.append({
                        'title' : filter_data.title,
                        'field_type' : field_type,
                        'choices' : [i for i in filter_data.choices(ch_inst)],
                    })
            data['filters'] = filters_list
                
        admin_ordering = register_app.get_ordering(request)
        if admin_ordering:
            data['order'] = {
            "name": 'o',
            'fields' : admin_ordering,
        }
        
        if ch_inst.search_fields:
            data['search'] = {
            "name": 'q'
        }
        
        if ch_inst.date_hierarchy:
            data['date_hierarchy_data'] = date_hierarchy(ch_inst)
        
        actions_list = []
        verbose_name_plural = model._meta.verbose_name_plural
        for _,name, desc in register_app.get_actions(request).values():
            actions_list.append({
                'name' : name,
                'desc' : desc % {'verbose_name_plural': verbose_name_plural} ,
            })
        if actions_list:
            data['actions'] = actions_list
        
        data['list_display'] = register_app.get_list_display(request)
        return Response(data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def posting_data(self, request, model, register_app, change, instance):
        fieldsets = register_app.get_fieldsets(request)
        ModelForm = register_app.get_form(
            request, obj=instance, change=change,
            fields=flatten_fieldsets(fieldsets)
        )
        
        form = ModelForm(request.data, request.FILES, instance=instance)
        formsets, _ = register_app._create_formsets(
            request,
            form.instance,
            change=change,
        )
        
        form_validated = form.is_valid()
        all_formset_validated = all_valid(formsets)
        if all_formset_validated and form_validated:
            instance = register_app.save_form(request, form, change=change)
            
            register_app.save_model(request, instance, form, change)
            register_app.save_related(request, form, formsets, change)
            
            change_message = register_app.construct_change_message(
                request, form, formsets, True
            )
            
            if change:
                register_app.log_change(request, instance, change_message)
            else:
                register_app.log_addition(request, instance, change_message)
            
            ser = self.get_serializer(model=model, instance=instance).data
            ser['perms'] = {
                "change": register_app.has_change_permission(request, instance),
                "delete": register_app.has_delete_permission(request, instance),
                "view": register_app.has_view_permission(request, instance)
            }  
            
            inline_instances = register_app.get_inline_instances(request, instance)
            if inline_instances and instance:
                self.get_inline_object_data(request, ser, inline_instances, instance)
            return ser
                    
        else:
            errors = form.errors or {}
            for inline_formset in formsets:
                if not inline_formset.is_valid() and inline_formset.errors:
                    inlines = errors.get('inlines', []) 
                    inlines.append({
                        'model_name' : inline_formset.model._meta.model_name,
                        'app_name' : inline_formset.model._meta.app_label,
                        'errors' : inline_formset.errors
                    })
                    errors['inlines'] = inlines
            raise ParseError(errors)
    
    @action(methods=['PATCH'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>\w+)/change')
    def patch_data(self, request, *args, **kwargs):
        model, register_app = self.get_model_register_admin()
        instance = self.get_object(register_app)
        change = True
        data = self.posting_data(request, model, register_app, change, instance)
        return Response(data)
        
    @action(methods=['POST'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/add')
    def create_data(self, request, *args, **kwargs):
        model, register_app = self.get_model_register_admin()
        change = False
        data = self.posting_data(request, model, register_app, change, None)
        return Response(data)
            
    @action(methods=['GET'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/fields')
    def list_field_meta(self, request, *args, **kwargs):
        model, register_app = self.get_model_register_admin()
        
        fieldsets = register_app.get_fieldsets(request)
        fieldsets = flatten_fieldsets(fieldsets)
        form = register_app.get_form(
            request, fields=fieldsets
        )()
        
        _, inline_instances = register_app._create_formsets(
            request, form.instance, change=False
        )
        
        readonly_fields = register_app.get_readonly_fields(request)
        admin_form = helpers.AdminForm(
            form,
            fieldsets,
            register_app.get_prepopulated_fields(request),
            readonly_fields,
            model_admin=register_app,
        )
        
        final_data = []
        admin_fields = admin_form.fields
        
        fields = model._meta.get_fields()
        register_app = admin.site._registry[model]
        
        final_data = {
            'fields' : self.get_fields_meta_data(
                request=request, fields=fields, 
                admin_fields=admin_fields
            ),
            'perms' : register_app.get_model_perms(request)
        }
        
        if inline_instances:
            self.get_inline_field_data(request, final_data, inline_instances)
            
        return Response(final_data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>\w+)')
    def retrieve_data(self, request, *args, **kwargs):
        model, register_app = self.get_model_register_admin()
        instance = self.get_object(register_app)
        
        ser = self.get_serializer(model=model, instance=instance).data
        ser['perms'] = {
            "add": register_app.has_add_permission(request),
            "change": register_app.has_change_permission(request, instance),
            "delete": register_app.has_delete_permission(request, instance),
            "view": register_app.has_view_permission(request, instance)
        }   
        
        inline_instances = register_app.get_inline_instances(request, instance)
        if inline_instances and instance:
            self.get_inline_object_data(request, ser, inline_instances, instance)
        
        return Response(ser, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/action',
            serializer_class=ActionSerializer)
    def action_perform(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ids = serializer.validated_data['ids']
        action = serializer.validated_data['action']
            
        try:
            ids = ids.split(',')
        except:
            raise ParseError({
                'message' : 'Error while split items ids.'
            })
            
        app_name = kwargs['app_name'].lower()
        model_name = kwargs['model_name'].lower()
        
        try:
            model = apps.get_model(app_name, model_name)
        except:
            raise ParseError({'message' : 'Model doesnot exist.'})

        try:
            queryset = model.objects.filter(id__in =ids)
        except:
            raise ParseError({'message' : 'Error due to getting items from ids.'})
        
        if not queryset.exists():
            raise ParseError({
                'message' : 'Items must be selected in order to perform actions on them. No items have been changed.'
            })
            
        try:
            register_app = admin.site._registry[model]
        except:
            raise ParseError({'message' : 'Admin register doesnot exist.'})
        
        actions = register_app.get_actions(request)
        action_v = actions.get(action)
        if not action_v:
            raise ParseError({
                'message' : 'Given action is not found.'
            })
        
        _, name, _ = action_v
        getattr(register_app, name)(request, queryset)
        all_messages = messages.get_messages(request)
        data = [{
            'message_content' : message.message, 
            'message_level' : level_to_human_readable(message.level)} 
            for message in all_messages
        ]
                
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['DELETE'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>[^/.]+)/delete-summary')
    def summary_of_delete_objects(self, request, *args, **kwargs):
        _, register_app = self.get_model_register_admin()
        instances = self.get_objects(register_app)
        
        summary_data = []
        for instance in instances:
            if not register_app.has_delete_permission(request, instance):
                raise PermissionDenied
            
            deleted_objects, model_count, perms_needed, protected = get_deleted_objects(
                [instance], request, register_app.admin_site
            )
            
            if perms_needed or protected:
                permission = False
            else:
                permission = True
            
            summary_data.append({
                'deleted_objects' : deleted_objects,
                'model_count' : { str(key) : value for key, value in model_count.items()},
                'permission' : permission,
                'id' : instance.id
            })
        return Response(summary_data)
    
    @transaction.atomic
    @action(methods=['DELETE'], detail=False, url_path=r'(?P<app_name>[\w-]+)/(?P<model_name>[\w-]+)/(?P<pk>\w+)/delete')
    def delete_objects(self, request, *args, **kwargs):
        _, register_app = self.get_model_register_admin()
        instances = self.get_objects(register_app)
        
        for instance in instances:
            if not register_app.has_delete_permission(request, instance):
                raise PermissionDenied
            
            _, _, perms_needed, protected = get_deleted_objects(
                [instance], request, register_app.admin_site
            )
            
            if perms_needed or protected:
                raise PermissionDenied
            instance.delete()
            
        message = f'The objects was deleted successfully.'
        return Response({'message':message})
