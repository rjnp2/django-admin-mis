# Generated by Django 4.2 on 2023-09-26 07:47

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_admin_mis.models
import django_admin_mis.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foreign1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Foreign2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='AllfieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('big_integer_field', models.BigIntegerField(help_text='help')),
                ('boolean_field', models.BooleanField(blank=True, default=False, help_text='help', null=True)),
                ('binary_field', models.BinaryField(help_text='help')),
                ('char_field', models.CharField(help_text='help', max_length=24)),
                ('char_choices_field', models.CharField(choices=[(1, 1)], help_text='help', max_length=24)),
                ('date_field', models.DateTimeField(help_text='help', validators=[django.core.validators.MinValueValidator(django_admin_mis.models.min_value), django.core.validators.MaxValueValidator(django_admin_mis.models.max_value)])),
                ('decimal_field', models.DecimalField(decimal_places=2, help_text='help', max_digits=12)),
                ('duration_field', models.DurationField(help_text='help')),
                ('email_field', models.EmailField(help_text='help', max_length=254)),
                ('file_field', models.FileField(help_text='icon to show in press release.', upload_to='website/icon/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'mp4'])])),
                ('float_field', models.FloatField(help_text='help', validators=[django.core.validators.MinValueValidator(django_admin_mis.models.get_min_value), django.core.validators.MaxValueValidator(django_admin_mis.models.get_max_value)])),
                ('generic_ip_field', models.GenericIPAddressField()),
                ('geometry_field', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('image_field', models.ImageField(upload_to='', validators=[django_admin_mis.validators.ImageValidator(max_size=(500, 500), min_size=(100, 100), size=500)])),
                ('integer_field', models.IntegerField()),
                ('json_field', models.JSONField(default=dict)),
                ('line_string_field', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('multi_line_string_field', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('multi_polygon_field', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('point_field', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('polygon_field', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('positive_big_integer_field', models.PositiveBigIntegerField()),
                ('positive_small_integer_field', models.PositiveSmallIntegerField()),
                ('positive_integer_field', models.PositiveIntegerField()),
                ('small_interger_field', models.SmallIntegerField()),
                ('time_field', models.TimeField()),
                ('url_field', models.URLField()),
                ('uuid_field', models.UUIDField()),
                ('pg_array_field', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('superuser', 'Superuser'), ('client', 'Client'), ('vendor', 'Vendor'), ('employee', 'Employee')], max_length=24), size=2)),
                ('pg_array_integer_field', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2)),
                ('pg_big_integer_range_field', django.contrib.postgres.fields.ranges.BigIntegerRangeField(null=True)),
                ('pg_date_range_field', django.contrib.postgres.fields.ranges.DateRangeField(null=True)),
                ('pg_date_time_range_field', django.contrib.postgres.fields.ranges.DateTimeRangeField(null=True)),
                ('pg_decimal_range_field', django.contrib.postgres.fields.ranges.DecimalRangeField(null=True)),
                ('pg_hstore_field', django.contrib.postgres.fields.hstore.HStoreField()),
                ('pg_integer_range_field', django.contrib.postgres.fields.ranges.IntegerRangeField()),
                ('phone_number', models.CharField(help_text='Enter your phone number.', max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be start with 9 and 10 digits allowed.', regex='^9\\d{9}$')], verbose_name='Phone Number')),
                ('foreign_field', models.ForeignKey(limit_choices_to={'name__icontains': 'anc'}, on_delete=django.db.models.deletion.CASCADE, related_name='Foreign1ss', to='django_admin_mis.foreign1')),
                ('many_to_many_field', models.ManyToManyField(to='django_admin_mis.foreign1')),
                ('o2o_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='django_admin_mis.foreign2')),
            ],
        ),
    ]