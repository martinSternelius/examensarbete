# -*- coding: utf-8 -*- 
from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from django.contrib.localflavor.se.se_counties import COUNTY_CHOICES
import re

def generate_rooms_choices(max_rooms_choice):
    '''
    Creates the list of choices to use for rooms selection fields
    '''
    
    rooms_choices = list()
    
    for x in range(2, (max_rooms_choice + 1) * 2):
        if(x % 2 > 0):
            floated_x = float(x)
            choice = floated_x/2
        else:
            choice = x/2
        
        choice = str(choice)
        rooms_choices.append((x, choice))
        
    return rooms_choices



HOUSING_TYPE_CHOICES = (
    (1, 'Hyresrätt'),
    (2, 'Bostadsrätt'),
    (4, 'Villa/Radhus')
)

def get_fields_by_prefix(prefix):
    '''
    Get fields names of the Listing model that have the provided prefix
    '''
    members = [attr for attr in dir(Listing()) if not callable(attr) and not attr.startswith("__")]
    fields = []
    for member in members:
        pattern = re.compile(prefix)
        if re.match(pattern, member):
            fields.append(member)
        
    return fields
    
    

BRF_STATUS_CHOICES = ((0, 'Ingen förening bildad'), (1, 'Förening Bildad'), (2, 'Blivande Bostadsrätt'))
BRF_WANTED_STATUS_CHOICES = ((0, 'Nej'), (1, 'Förening Bildad eller Blivande Bostadsrätt'), (2, 'Blivande Bostadsrätt'))
FLOOR_CHOICES = ((0, 'Inget krav'), (1, 'Ej nedre botten'))
    
MAX_ROOMS_CHOICE = 6
rooms_choices = generate_rooms_choices(MAX_ROOMS_CHOICE)

class Listing(models.Model):
    '''
    This model represents a listing for a housing trade
    It consists of data about the housing offered (o), and data about the housing wanted (w)
    '''
    
    creation_datetime = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User)
    
    o_county = CharField(max_length=255, verbose_name='Län', choices=COUNTY_CHOICES)
    o_street_address = models.CharField(max_length=255, verbose_name='Gatuadress')
    o_rooms = models.PositiveIntegerField(choices=rooms_choices, verbose_name='Antal rum') # The number of rooms times 2, to avoid having to use floats or decimals
    o_area = models.PositiveIntegerField(verbose_name='Yta') # area in square meters
    o_type = models.PositiveIntegerField(choices=HOUSING_TYPE_CHOICES, verbose_name = 'Bostadstyp')
    o_rent = models.PositiveIntegerField(verbose_name = 'Hyra/Avgift')
    o_description = models.TextField(verbose_name='Beskrivning')
    o_brf_status = models.PositiveIntegerField(choices=BRF_STATUS_CHOICES, verbose_name='Om hyresrätt, är det blivande bostadsrätt?', blank=True)
    o_floor_no = models.IntegerField(verbose_name='Våning')
    o_has_fireplace = models.BooleanField(verbose_name='Öppen spis')
    o_has_balcony = models.BooleanField(verbose_name='Balkong')
    o_has_elevator = models.BooleanField(verbose_name='Hiss')
    
    w_county = CharField(max_length=255, verbose_name='Län', choices=COUNTY_CHOICES)
    w_min_rooms = models.PositiveIntegerField(choices=rooms_choices, verbose_name='Minsta antal rum')
    w_min_area = models.PositiveIntegerField(verbose_name='Minsta yta') # area in square meters
    w_max_rent = models.PositiveIntegerField(verbose_name='Max hyra')
    w_types = models.CommaSeparatedIntegerField(max_length=255, verbose_name='Önskade bostadstyper')
    w_brf_status = models.PositiveIntegerField(choices=BRF_WANTED_STATUS_CHOICES, verbose_name='Blivande bostadsrätt?', blank=True)
    w_has_fireplace = models.NullBooleanField(verbose_name='Öppen spis')
    w_has_balcony = models.NullBooleanField(verbose_name='Balkong')
    w_has_elevator = models.NullBooleanField(verbose_name='Hiss')
    w_not_bottom_floor = models.NullBooleanField(verbose_name='Våning', choices=FLOOR_CHOICES)