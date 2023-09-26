from datetime import date, datetime
from django.contrib.gis.db import models
from django.contrib.postgres import fields
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)
from .validators import ImageValidator

class ForeignModel1(models.Model):
    name = models.CharField(max_length=255)  # Adjusted field name and added max_length

class ForeignModel2(models.Model):
    name = models.CharField(max_length=255)  # Adjusted field name and added max_length

def min_year():
    return datetime.now().replace(year=datetime.now().year - 100)

def max_year():
    return datetime.now().replace(year=datetime.now().year - 18)

def min_date():
    return date.today().replace(year=date.today().year - 100)

def max_date():
    return date.today().replace(year=date.today().year - 18)

def get_min_value():
    return 100

def get_max_value():
    return 200

class AllFieldModel(models.Model):
    big_integer_field = models.BigIntegerField(help_text='A help message')  # Added a helpful help_text
    boolean_field = models.BooleanField(
        help_text='A help message',
        default=False,
        null=True,
        blank=True
    )
    binary_field = models.BinaryField(help_text='A help message')  # Added a helpful help_text

    char_field = models.CharField(help_text='A help message', max_length=255)  # Added max_length and a helpful help_text
    char_choices_field = models.CharField(help_text='A help message', max_length=255, choices=((1, 1),))  # Added max_length and a helpful help_text

    date_field = models.DateField(
        help_text='A help message',
        validators=[
            MinValueValidator(min_year), 
            MaxValueValidator(max_year)
        ]
    )
    date_time_field = models.DateTimeField(
        help_text='A help message',
        validators=[
            MinValueValidator(min_date),
            MaxValueValidator(max_date)
        ]
    )
    decimal_field = models.DecimalField(help_text='A help message', max_digits=12, decimal_places=2)  # Added max_digits and decimal_places
    duration_field = models.DurationField(help_text='A help message')  # Added a helpful help_text

    email_field = models.EmailField(help_text='A help message')

    file_field = models.FileField(
        upload_to='website/icon/', 
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'mp4'])
        ],
        help_text='Icon to show in press release.'  # Adjusted help_text
    )
    float_field = models.FloatField(
        help_text='A help message',
        validators=[
            MinValueValidator(get_min_value), 
            MaxValueValidator(get_max_value)
        ]
    )
    foreign_field = models.ForeignKey(
        ForeignModel1, 
        on_delete=models.CASCADE,
        limit_choices_to={'name__icontains': 'anc'},
        related_name='foreign_model1_set'  # Adjusted related_name
    )

    generic_ip_field = models.GenericIPAddressField()
    geometry_field = models.GeometryField(help_text='A help message')  # Added a helpful help_text

    image_field = models.ImageField(
        validators=[
            ImageValidator(
                size=500,
                min_size=(100, 100),
                max_size=(500, 500)
            )
        ],
        help_text='An image field with validation.'  # Adjusted help_text
    )
    integer_field = models.IntegerField(help_text='A help message')

    json_field = models.JSONField(default=dict)

    line_string_field = models.LineStringField(help_text='A help message')  # Added a helpful help_text

    many_to_many_field = models.ManyToManyField(ForeignModel1)
    multi_line_string_field = models.MultiLineStringField(help_text='A help message')  # Added a helpful help_text
    multi_polygon_field = models.MultiPolygonField(help_text='A help message')  # Added a helpful help_text

    o2o_field = models.OneToOneField(ForeignModel2, on_delete=models.CASCADE)

    point_field = models.PointField(help_text='A help message')  # Added a helpful help_text
    polygon_field = models.PolygonField(help_text='A help message')  # Added a helpful help_text
    positive_big_integer_field = models.PositiveBigIntegerField(help_text='A help message')  # Added a helpful help_text
    positive_small_integer_field = models.PositiveSmallIntegerField(help_text='A help message')  # Added a helpful help_text
    positive_integer_field = models.PositiveIntegerField(help_text='A help message')  # Added a helpful help_text

    small_integer_field = models.SmallIntegerField(help_text='A help message')

    time_field = models.TimeField(help_text='A help message')  # Added a helpful help_text

    url_field = models.URLField(help_text='A help message')  # Added a helpful help_text
    uuid_field = models.UUIDField(help_text='A help message')  # Added a helpful help_text

    user_type_choices = (
        ('superuser', 'Superuser'),
        ('client', 'Client'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
    )

    pg_array_field = fields.ArrayField(
        size=2,
        base_field=models.CharField(
            max_length=255,
            choices=user_type_choices,
            help_text='Choose from user types.'  # Adjusted help_text
        )
    ) 

    pg_array_integer_field = fields.ArrayField(
        size=2, 
        base_field=models.IntegerField()
    )

    pg_big_integer_range_field = fields.BigIntegerRangeField(null=True)

    pg_date_range_field = fields.DateRangeField(null=True)
    pg_date_time_range_field = fields.DateTimeRangeField(null=True)
    pg_decimal_range_field = fields.DecimalRangeField(null=True)
    pg_decimal_range_field.base_field = models.DecimalField(max_digits=12, decimal_places=2)

    pg_hstore_field = fields.HStoreField(help_text='A help message')  # Added a helpful help_text

    pg_integer_range_field = fields.IntegerRangeField(help_text='A help message')  # Added a helpful help_text

    phone_regex = RegexValidator(
        regex=r'^9\d{9}$',
        message="Phone number must start with 9 and have 10 digits."  # Adjusted error message
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=14,
        unique=True,
        verbose_name='Phone Number',
        help_text='Enter your phone number.'
    )
