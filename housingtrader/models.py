# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.localflavor.se.forms import SEPostalCodeField, SECountySelect

def generate_rooms_choices(max_rooms_choice):
    '''
    Creates the list of choices to use for rooms selection fields
    '''
    
    rooms_choices = list()
    
    for x in range(2, max_rooms_choice * 2):
        if(x % 2 > 0):
            floated_x = float(x)
            choice = floated_x/2
        else:
            choice = x/2
        
        choice = str(choice)
        rooms_choices.append((choice, x))
        
    return rooms_choices

class Listing(models.Model):
    '''
    This model represents a listing for a housing trade
    It consists of data about the housing offered (o), and data about the housing wanted (w)
    '''
    HOUSING_TYPE_CHOICES = (
        (0, 'Hyresrätt'),
        (1, 'Bostadsrätt'),
        (2, 'Villa/Radhus')
    )
    
    BRF_STATUS_CHOICES = ((0, 'Ej bildad'), (1, 'Förening Bildad'), (2, 'Blivande Bostadsrätt'))
    BRF_WANTED_STATUS_CHOICES = ((0, 'Nej'), (1, 'Förening Bildad eller Blivande Bostadsrätt'), (2, 'Blivande Bostadsrätt'))
    
    MAX_ROOMS_CHOICE = 6
    rooms_choices = generate_rooms_choices(MAX_ROOMS_CHOICE)
    
    creation_datetime = models.DateTimeField(auto_now_add=True)
    o_county = SECountySelect()
    o_street_address = models.CharField(max_length=255)
    o_postal_code = SEPostalCodeField
    o_rooms = models.PositiveIntegerField(choices = rooms_choices) # The number of rooms times 2, to avoid having to use floats or decimals
    o_area = models.PositiveIntegerField() # area in square meters
    o_type = models.PositiveIntegerField(choices=HOUSING_TYPE_CHOICES)
    o_rent = models.PositiveIntegerField()
    o_description = models.TextField()
    o_brf_status = models.PositiveIntegerField(choices=BRF_STATUS_CHOICES)
    o_floor_no = models.IntegerField()
    o_has_fireplace = models.BooleanField()
    o_has_balcony = models.BooleanField()
    o_has_elevator = models.BooleanField()
    
    w_county = SECountySelect()
    w_min_rooms = models.PositiveIntegerField(choices = rooms_choices)
    w_min_area = models.PositiveIntegerField() # area in square meters
    w_max_rent = models.PositiveIntegerField()
    w_types = models.PositiveIntegerField(choices=HOUSING_TYPE_CHOICES)
    w_brf_status = models.PositiveIntegerField(choices=BRF_WANTED_STATUS_CHOICES)
    w_has_fireplace = models.NullBooleanField()
    w_has_balcony = models.NullBooleanField()
    w_has_elevator = models.NullBooleanField()
    w_not_bottom_floor = models.NullBooleanField()