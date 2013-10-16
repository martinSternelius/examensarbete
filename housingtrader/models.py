# -*- coding: utf-8 -*- 
from django.db import models
from django.db.models.fields import CharField
from examensarbete.settings import AUTH_USER_MODEL
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

TYPE_TENANCY = 1
TYPE_BRF = 2
TYPE_HOUSE = 4

HOUSING_TYPE_CHOICES = (
    (TYPE_TENANCY, 'Hyresrätt'),
    (TYPE_BRF, 'Bostadsrätt'),
    (TYPE_HOUSE, 'Villa/Radhus')
)

def get_listing_fields_by_prefix(prefix):
    '''
    Get field names of the Listing model that have the provided prefix
    '''
    members = [attr for attr in dir(Listing()) if not callable(attr) and not attr.startswith("__")]
    fields = []
    for member in members:
        pattern = re.compile(prefix)
        if re.match(pattern, member):
            fields.append(member)
        
    return fields
    
    
BRF_NONE = 0
BRF_FORMED = 1
BRF_TO_BE = 2

BRF_STATUS_CHOICES = ((BRF_NONE, 'Ingen förening bildad'), (BRF_FORMED, 'Förening Bildad'), (BRF_TO_BE, 'Blivande Bostadsrätt'))
BRF_WANTED_STATUS_CHOICES = ((BRF_NONE, 'Nej'), (BRF_FORMED, 'Förening Bildad eller Blivande Bostadsrätt'), (BRF_TO_BE, 'Blivande Bostadsrätt'))
FLOOR_CHOICES = ((0, 'Inget krav'), (1, 'Ej nedre botten'))
    
MAX_ROOMS_CHOICE = 10
rooms_choices = generate_rooms_choices(MAX_ROOMS_CHOICE)

class Listing(models.Model):
    '''
    This model represents a listing for a housing trade
    It consists of data about the housing offered (o), and data about the housing wanted (w)
    '''
    
    creation_datetime = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(AUTH_USER_MODEL)
    
    o_county = CharField(max_length=255, verbose_name='Län', choices=COUNTY_CHOICES)
    o_street_address = models.CharField(max_length=255, verbose_name='Gatuadress')
    o_postal_code = models.CharField(max_length=255, verbose_name='Postnummer')
    o_postal_town = models.CharField(max_length=255, verbose_name='Postort')
    o_rooms = models.PositiveIntegerField(choices=rooms_choices, verbose_name='Antal rum') # The number of rooms times 2, to avoid having to use floats or decimals
    o_area = models.PositiveIntegerField(verbose_name='Yta') # area in square meters
    o_type = models.PositiveIntegerField(choices=HOUSING_TYPE_CHOICES, verbose_name='Bostadstyp')
    o_rent = models.PositiveIntegerField(verbose_name = 'Hyra/Avgift')
    o_description = models.TextField(verbose_name='Beskrivning')
    o_brf_status = models.PositiveIntegerField(choices=BRF_STATUS_CHOICES, verbose_name='Om hyresrätt, är det blivande bostadsrätt?', null=True, blank=True)
    o_floor_no = models.IntegerField(verbose_name='Våning')
    o_has_fireplace = models.BooleanField(verbose_name='Öppen spis', default=False)
    o_has_balcony = models.BooleanField(verbose_name='Balkong', default=False)
    o_has_elevator = models.BooleanField(verbose_name='Hiss', default=False)
    
    w_county = CharField(max_length=255, verbose_name='Län', choices=COUNTY_CHOICES)
    w_min_rooms = models.PositiveIntegerField(choices=rooms_choices, verbose_name='Minsta antal rum')
    w_min_area = models.PositiveIntegerField(verbose_name='Minsta yta') # area in square meters
    w_max_rent = models.PositiveIntegerField(verbose_name='Max hyra')
    w_types = models.CommaSeparatedIntegerField(max_length=255, verbose_name='Önskade bostadstyper')
    w_brf_status = models.PositiveIntegerField(choices=BRF_WANTED_STATUS_CHOICES, verbose_name='Blivande bostadsrätt?', null=True, blank=True)
    w_has_fireplace = models.BooleanField(verbose_name='Öppen spis')
    w_has_balcony = models.BooleanField(verbose_name='Balkong')
    w_has_elevator = models.BooleanField(verbose_name='Hiss')
    w_not_bottom_floor = models.BooleanField(verbose_name='Våning', choices=FLOOR_CHOICES)
    
    def find_matches(self):
        '''
        Finds listings of other users where the offered parameters match this listing's wanted parameters
        '''
        
        wanted_types = str(self.w_types).split(',')
        
        matches = Listing.objects.filter(
            o_county = self.w_county,
            o_rooms__gte = self.w_min_rooms,
            o_area__gte = self.w_min_area,
            o_rent__lte = self.w_max_rent,
            o_type__in = wanted_types
        ).exclude(user = self.user)
        
        if self.w_brf_status is not None:
            matches = matches.filter(
                o_brf_status__gte = self.w_brf_status
            )
            
        if self.w_has_fireplace:
            matches = matches.filter(o_has_fireplace = True)
            
        if self.w_has_elevator:
            matches = matches.filter(o_has_elevator = True)
            
        if self.w_has_balcony:
            matches = matches.filter(o_has_balcony = True)
            
        if self.w_not_bottom_floor:
            matches = matches.filter(o_floor_no__gt = 0)
            
        return matches
    
    def find_reverse_matches(self):
        '''
        Finds listings of other users where the wanted parameters match this listing's offered parameters
        '''
        
        matches = Listing.objects.filter(
            w_county = self.o_county,
            w_min_rooms__lte = self.o_rooms,
            w_min_area__lte = self.o_area,
            w_max_rent__gte = self.o_rent,
            w_has_fireplace__lte = self.o_has_fireplace,
            w_has_elevator__lte = self.o_has_elevator,
            w_has_balcony__lte = self.w_has_balcony
        ).exclude(user = self.user)
        
        final_matches = []
        for listing in matches:
            if listing.w_not_bottom_floor and self.o_floor_no < 1:
                continue
            
            wanted_types = str(listing.w_types).split(',')
            
            if str(self.o_type) not in wanted_types:
                continue
            
            if listing.w_brf_status is not None and self.o_brf_status < listing.w_brf_status:
                continue
            
            final_matches.append(listing)
                
        return final_matches
    
    def find_mutual_matches(self):
        '''
        Finds listings where the offered and wanted parameters match each other
        '''
        
        matches= self.find_matches()
        reverse_matches = self.find_reverse_matches()
        
        return set(matches).intersection(reverse_matches)
    
    def get_w_types_display(self):
        '''
        Returns a comma separated string of housing type values
        '''
        
        housing_types = dict(HOUSING_TYPE_CHOICES)
        wanted_type_ids = str(self.w_types).split(',')
        wanted_types_verbose = []
        for type_id in wanted_type_ids:
            type_id = type_id.strip()
            housingtype = housing_types[int(type_id)]
            wanted_types_verbose.append(housingtype)
            
        return ', '.join(wanted_types_verbose)
    
    def __unicode__(self):
        return self.o_street_address
    
    class Meta:
        verbose_name='Annons'
        verbose_name_plural='Annonser'
        
class TradeRequest(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(Listing, related_name='trade_requests_sent')
    receiver = models.ForeignKey(Listing, related_name='trade_requests_received')
    viewed_by_receiver = models.BooleanField(default=False)
    declined_by_receiver = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.requester) + ' bytes mot ' + str(self.receiver)
    
    class Meta:
        unique_together = ('requester', 'receiver')
    