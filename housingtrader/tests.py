# -*- coding: utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from housingtrader.models import Listing, TYPE_BRF, TYPE_TENANCY
from housingtrader.forms import CompleteListingForm
from django.http.request import QueryDict

class ListingFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@example.com', 'password')
        
    def tearDown(self):
        self.user.delete()
        
    def test_save(self):
        '''
        Assertion: The form correctly processes the w_housing_types fields and saves the list of number as a string of comma separated numbers
        '''
        query_string = 'w_min_rooms=8&w_has_elevator=2&o_rent=6000&o_postal_code=14414&o_has_balcony=on&o_area=50&w_county=AB&o_brf_status=0&w_has_fireplace=2&o_floor_no=5&w_types=1&w_types=2&w_max_rent=10000&o_street_address=Testgatan+1&o_type=1&w_has_balcony=2&o_rooms=5&o_has_elevator=on&o_description=En+testl%C3%A4genhet&w_not_bottom_floor=1&w_min_area=60&o_county=AB&w_brf_status=1'
        form = CompleteListingForm(data=QueryDict(query_string), user=self.user)
        
        form.save()
        
        listing = Listing.objects.get(o_description='En testlägenhet')
        self.assertEqual(listing.w_types, '1,2')
        
class ListingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@example.com', 'password')
        
        listing = Listing()
        listing.o_area = 33
        listing.o_brf_status = None
        listing.o_county = 'AB'
        listing.o_description = 'Min'
        listing.o_floor_no = -1
        listing.o_has_balcony = 1
        listing.o_has_elevator = 0
        listing.o_has_fireplace = 0
        listing.o_postal_code = '16846'
        listing.o_rent = 1722
        listing.o_rooms = 1
        listing.o_street_address = 'Arvid Mörnes väg 42'
        listing.o_type = TYPE_BRF
        listing.w_brf_status = None
        listing.w_county = 'AB'
        listing.w_has_balcony = None
        listing.w_has_elevator = None
        listing.w_has_fireplace = None
        listing.w_max_rent = 5000
        listing.w_min_area = 33
        listing.w_min_rooms = 1
        listing.w_not_bottom_floor = None
        listing.w_types = str(TYPE_TENANCY) + str(TYPE_BRF)
        
        listing.user = self.user
        
        self.listing = listing
        self.listing.save()
        
    def test_find_match(self):
        user = User.objects.create_user('tester2', 'test2@example.com', 'password')
        
        listing = Listing()
        listing.o_area = 33
        listing.o_brf_status = None
        listing.o_county = 'AB'
        listing.o_description = 'Matching'
        listing.o_floor_no = 1
        listing.o_has_balcony = 1
        listing.o_has_elevator = 0
        listing.o_has_fireplace = 0
        listing.o_postal_code = '16846'
        listing.o_rent = 1722
        listing.o_rooms = 1
        listing.o_street_address = 'Arvid Mörnes väg 42'
        listing.o_type = TYPE_BRF
        listing.w_brf_status = None
        listing.w_county = 'AB'
        listing.w_has_balcony = None
        listing.w_has_elevator = None
        listing.w_has_fireplace = None
        listing.w_max_rent = 5000
        listing.w_min_area = 33
        listing.w_min_rooms = 1
        listing.w_not_bottom_floor = None
        listing.w_types = str(TYPE_TENANCY) + str(TYPE_BRF)
        
        listing.user = user
        
        listing.save()
        
        matches = self.listing.find_matches()
        
        self.assertTrue(listing in matches)
        
        
    
    
