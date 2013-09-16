# -*- coding: utf-8 -*- 
from django.db import models

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
    
    BRF_STATUS_CHOICES = ((0, 'Ej bildad'), (1, 'Blivande'), (2, 'Bildad'))
    
    MAX_ROOMS_CHOICE = 6
    
    creation_datetime = models.DateTimeField(auto_now_add=True)
    o_street_address = models.CharField(max_length=255)
    o_postal_code = models.CharField(max_length=255)
    o_rooms = models.PositiveIntegerField(choices = generate_rooms_choices(MAX_ROOMS_CHOICE)) # The number of rooms times 2, to avoid having to use floats or decimals
    o_area = models.PositiveIntegerField() # area in square meters
    o_type = models.PositiveIntegerField(choices=HOUSING_TYPE_CHOICES)
    o_description = models.TextField()
    o_brf_status = models.PositiveIntegerField(choices = BRF_STATUS_CHOICES)