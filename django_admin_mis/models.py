from datetime import date, datetime

from django.contrib.gis.db import models
from django.contrib.postgres import fields
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)

from .validators import ImageValidator


# Create your models here.
class Foreign1(models.Model):
   name = models.CharField()

class Foreign2(models.Model):
   name = models.CharField()
   
def min_year():
   return datetime.now().replace(year = datetime.now().year - 100)

def max_year():
   return datetime.now().replace(year = datetime.now().year - 18)

def min_value():
   return date.today().replace(year = date.today().year - 100)

def max_value():
   return date.today().replace(year = date.today().year - 18)
 
def get_min_value():
   return 100

def get_max_value():
   return 200

class AllfieldModel(models.Model):
   big_integer_field = models.BigIntegerField(help_text='help')
   boolean_field = models.BooleanField(help_text='help', default=False, null=True, blank=True)
   binary_field = models.BinaryField(help_text='help')
   
   char_field = models.CharField(help_text='help', max_length=24)
   char_choices_field = models.CharField(help_text='help', max_length=24, choices=((1,1),))
   
   date_field = models.DateField(
      help_text='help', 
      validators = [
         MinValueValidator(min_year), 
         MaxValueValidator(max_year)
      ]
   )
   date_field = models.DateTimeField(
      help_text='help', 
      validators = [
         MinValueValidator(min_value), 
         MaxValueValidator(max_value)
      ]
   )
   decimal_field = models.DecimalField(help_text='help', max_digits=12, decimal_places=2)
   duration_field = models.DurationField(help_text='help')
   
   email_field = models.EmailField(help_text='help')
   
   file_field = models.FileField(
      upload_to='website/icon/', 
      validators=[
         FileExtensionValidator(allowed_extensions=['pdf', 'mp4'])
      ],
      help_text='icon to show in press release.'
   )
   float_field = models.FloatField(help_text='help',
      validators = [
         MinValueValidator(get_min_value), 
         MaxValueValidator(get_max_value)
      ]
   )
   foreign_field = models.ForeignKey(Foreign1, on_delete=models.CASCADE,
                  limit_choices_to={'name__icontains':'anc'},
                  related_name='Foreign1ss')
   
   generic_ip_field = models.GenericIPAddressField()
   geometry_field = models.GeometryField()
   
   image_field = models.ImageField(
      validators=[ImageValidator(
                size=500,
                min_size=(100, 100),
                max_size=(500, 500))
      ],
   )
   integer_field = models.IntegerField()
   
   json_field = models.JSONField(default=dict)
   
   line_string_field = models.LineStringField()
   
   many_to_many_field = models.ManyToManyField(Foreign1)
   multi_line_string_field = models.MultiLineStringField()
   multi_polygon_field = models.MultiPolygonField()
   
   o2o_field = models.OneToOneField(Foreign2, on_delete=models.CASCADE)
   
   point_field = models.PointField()
   polygon_field = models.PolygonField()
   positive_big_integer_field = models.PositiveBigIntegerField()
   positive_small_integer_field = models.PositiveSmallIntegerField()
   positive_integer_field = models.PositiveIntegerField()
   
   small_interger_field = models.SmallIntegerField()
   
   time_field = models.TimeField()
   
   url_field = models.URLField()
   uuid_field = models.UUIDField()
   
   user_type_choices = (
        ('superuser','Superuser'),
        ('client','Client'),
        ('vendor','Vendor'),
        ('employee','Employee'),
   )
   pg_array_field = fields.ArrayField(
      size=2, 
      base_field = models.CharField(
         max_length=24, choices=user_type_choices
      )
   ) 
   pg_array_integer_field = fields.ArrayField(
      size=2, 
      base_field = models.IntegerField()
   )
   
   pg_big_integer_range_field = fields.BigIntegerRangeField(null=True)
   
   pg_date_range_field = fields.DateRangeField(null=True)
   pg_date_time_range_field = fields.DateTimeRangeField(null=True)
   pg_decimal_range_field = fields.DecimalRangeField(null=True)
   pg_decimal_range_field.base_field= models.DecimalField(max_digits=12, decimal_places=2)
   
   pg_hstore_field = fields.HStoreField()
   
   pg_integer_range_field = fields.IntegerRangeField()
   
   # Validating the phone number.
   phone_regex = RegexValidator(
      regex=r'^9\d{9}$', 
      message="Phone number must be start with 9 and 10 digits allowed."
   )
   phone_number = models.CharField(
      validators=[phone_regex], max_length=14, 
      unique=True, verbose_name='Phone Number',
      help_text='Enter your phone number.'
   )
   