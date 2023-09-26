import json
import re

from django.contrib import messages


def simple_field_form(field):
    field_name = field.description.lower()
    field_name = re.sub(r'\([^)^(]*\)', '', field_name)
    field_name = re.sub(r'\([^)^(]*\)', '', field_name)
    field_name = re.sub(r'\s+', ' ', field_name).strip()
    
    if field.get_internal_type() == 'DateTimeField':
        field_name += ' time'
        
    if field.get_internal_type() == 'GeometryField':
        field_name = field.geom_type.lower()
    
    return field_name

def level_to_human_readable(level):
    if level == messages.SUCCESS:
        return "Success"
    elif level == messages.INFO:
        return "Information"
    elif level == messages.WARNING:
        return "Warning"
    elif level == messages.ERROR:
        return "Error"
    else:
        return "Unknown"
    
def python_validator_dict(field):
    validators = []
    try:
        for validator in field.validators:
            inside_dict = {}
            if hasattr(validator, 'message'):
                inside_dict['message'] = validator.message
                
            if hasattr(validator, 'messages'):
                inside_dict['messages'] = validator.messages
                
            if hasattr(validator, 'code'):
                inside_dict['code'] = validator.code
            
            if hasattr(validator, 'limit_value'):
                if callable(validator.limit_value):
                    inside_dict['limit_value'] = validator.limit_value()
                else:
                    inside_dict['limit_value'] = validator.limit_value
                
            if hasattr(validator, 'max_digits'):
                inside_dict['max_digits'] = validator.max_digits
                
            if hasattr(validator, 'decimal_places'):
                inside_dict['decimal_places'] = validator.decimal_places
                
            if hasattr(validator, 'regex'):
                inside_dict['regex'] = str(validator.regex.pattern)
                
            if hasattr(validator, 'size'):
                inside_dict['size'] = validator.size
                
            if hasattr(validator, 'min_size'):
                inside_dict['min_size'] = validator.min_size
                
            if hasattr(validator, 'allowed_extensions'):
                inside_dict['allowed_extensions'] = validator.allowed_extensions
                
            if hasattr(validator, 'max_size'):
                inside_dict['max_size'] = validator.max_size
            
            validators.append(inside_dict)
            
    except Exception as e:
        print(e)
        
    return validators

def get_default_values(field):
    if field.has_default():
        defaults = field._get_default() 
        
        try:
            json.dumps(defaults)
        except Exception as e:
            print(f'error due to {e} in default')
            defaults = None
    else:
        defaults = None
        
    return defaults