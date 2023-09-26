import json
import re
from django.contrib import messages

def format_field_name(field):
    """
    Format a field's name for display.
    """
    field_name = field.description.lower()
    field_name = re.sub(r'\([^)^(]*\)', '', field_name)
    field_name = re.sub(r'\([^)^(]*\)', '', field_name)
    field_name = re.sub(r'\s+', ' ', field_name).strip()
    
    if field.get_internal_type() == 'DateTimeField':
        field_name += ' time'
        
    if field.get_internal_type() == 'GeometryField':
        field_name = field.geom_type.lower()
    
    return field_name

def format_message_level(level):
    """
    Convert a message level to a human-readable format.
    """
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
    
def get_validator_info(field):
    """
    Extract information about validators applied to a field and return as a list of dictionaries.
    """
    validators_info = []
    try:
        for validator in field.validators:
            validator_info = {}
            
            if hasattr(validator, 'message'):
                validator_info['message'] = validator.message
                
            if hasattr(validator, 'messages'):
                validator_info['messages'] = validator.messages
                
            if hasattr(validator, 'code'):
                validator_info['code'] = validator.code
            
            if hasattr(validator, 'limit_value'):
                if callable(validator.limit_value):
                    validator_info['limit_value'] = validator.limit_value()
                else:
                    validator_info['limit_value'] = validator.limit_value
                
            if hasattr(validator, 'max_digits'):
                validator_info['max_digits'] = validator.max_digits
                
            if hasattr(validator, 'decimal_places'):
                validator_info['decimal_places'] = validator.decimal_places
                
            if hasattr(validator, 'regex'):
                validator_info['regex'] = str(validator.regex.pattern)
                
            if hasattr(validator, 'size'):
                validator_info['size'] = validator.size
                
            if hasattr(validator, 'min_size'):
                validator_info['min_size'] = validator.min_size
                
            if hasattr(validator, 'allowed_extensions'):
                validator_info['allowed_extensions'] = validator.allowed_extensions
                
            if hasattr(validator, 'max_size'):
                validator_info['max_size'] = validator.max_size
            
            validators_info.append(validator_info)
            
    except Exception as e:
        print(e)
        
    return validators_info

def get_default_value(field):
    """
    Get the default value of a field, handling cases where the default may be complex.
    """
    if field.has_default():
        default_value = field._get_default() 
        
        try:
            json.dumps(default_value)
        except Exception as e:
            print(f'Error due to {e} in default')
            default_value = None
    else:
        default_value = None
        
    return default_value
