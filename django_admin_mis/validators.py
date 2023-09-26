import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class ImageValidator:
    messages = {
        "dimensions": 'Image dimensions must be greater than or equal to %(width)s width x %(height)s height, but your image size is %(value_width)s width x %(value_height)s height.',
        "max_dimensions": 'Image dimensions must be less than %(width)s width x %(height)s height, but your image size is %(value_width)s width x %(value_height)s height.',
        "size": "File must be smaller than or equal to than > %(size)skB."
    }

    def __init__(self, size : int=None, min_size: tuple=None,
                    max_size: tuple=None):
        self.size = size

        if min_size:
            if type(min_size) != tuple:
                raise TypeError('min_size type must be tuple.')
            
            if len(min_size) != 2:
                raise ValueError('min_size len must be 2.')
            
            item_type = set([type(item) for item in min_size]).pop()
            if item_type != int:
                raise ValueError(f'item inside min_size type must be int {item_type}.')
        self.min_size = min_size

        if max_size:
            if type(max_size) != tuple:
                raise TypeError('max_size type must be tuple.')
            
            if len(max_size) != 2:
                raise ValueError('max_size len must be 2.')
            
            item_type = set([type(item) for item in max_size]).pop()
            if item_type != int:
                raise ValueError('item inside max_size type must be int.')
        self.max_size = max_size

    def __call__(self, value):
        if self.size is not None and value.size < self.size:
            raise ValidationError(
                self.messages['size'],
                params={
                    'size': float(self.size)/1024,
                    'value': value,
                }
            )
        
        width = value.image.width if hasattr(value, 'image') else value.width
        height = value.image.height if hasattr(value, 'image') else value.height
        if (self.min_size is not None and
                (width < self.min_size[0] or height < self.min_size[1])):
            raise ValidationError(
                self.messages['dimensions'],
                params={
                    'width': self.min_size[0],
                    'value_width': width,
                    'height': self.min_size[1],
                    'value_height': height,
                    'value': value,
                }
            )
        
        if (self.max_size is not None and
                (width > self.max_size[0] or height > self.max_size[1])):
            raise ValidationError(
                self.messages['max_dimensions'],
                params={
                    'width': self.max_size[0],
                    'value_width': width,
                    'height': self.max_size[1],
                    'value_height': height,
                    'value': value,
                }
            )

