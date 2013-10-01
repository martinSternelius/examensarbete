# -*- coding: utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from housingtrader.models import Listing, TYPE_BRF, TYPE_TENANCY, TYPE_HOUSE, BRF_NONE, BRF_FORMED
from housingtrader.forms import CompleteListingForm
from django.http.request import QueryDict

class ListingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 'test@example.com', 'password')
        
    def tearDown(self):
        self.user.delete()
        
    def test_create_listing_view(self):
        '''
        Assertion: A logged in user that sends valid POST data to create_listing will result in a listing correctly saved in the database.
        '''
        client = Client()
        client.login(username='tester', password='password')
        
        asserted_listing = Listing()
        asserted_listing.o_area = 33
        asserted_listing.o_brf_status = None
        asserted_listing.o_county = 'AB'
        asserted_listing.o_description = 'Min'
        asserted_listing.o_floor_no = -1
        asserted_listing.o_has_balcony = 1
        asserted_listing.o_has_elevator = 0
        asserted_listing.o_has_fireplace = 0
        asserted_listing.o_postal_code = '16846'
        asserted_listing.o_rent = 1722
        asserted_listing.o_rooms = 2
        asserted_listing.o_street_address = 'Klientvägen 1'
        asserted_listing.o_type = TYPE_BRF
        asserted_listing.w_brf_status = None
        asserted_listing.w_county = 'AB'
        asserted_listing.w_has_balcony = False
        asserted_listing.w_has_elevator = False
        asserted_listing.w_has_fireplace = False
        asserted_listing.w_max_rent = 5000
        asserted_listing.w_min_area = 33
        asserted_listing.w_min_rooms = 2
        asserted_listing.w_not_bottom_floor = False
        asserted_listing.w_types = ','.join([str(TYPE_TENANCY), str(TYPE_BRF)])
        
        data = {
            'o_area' : 33,
            'o_brf_status' : '',
            'o_county' : 'AB',
            'o_description' : 'Min',
            'o_floor_no' : -1,
            'o_has_balcony' : 1,
            'o_has_elevator' : 0,
            'o_has_fireplace' : 0,
            'o_postal_code' : '16846',
            'o_rent' : 1722,
            'o_rooms' : 2,
            'o_street_address' : 'Klientvägen 1',
            'o_type' : TYPE_BRF,
            'w_brf_status' : '',
            'w_county' : 'AB',
            'w_has_balcony' : 0,
            'w_has_elevator' : 0,
            'w_has_fireplace' : 0,
            'w_max_rent' : 5000,
            'w_min_area' : 33,
            'w_min_rooms' : 2,
            'w_not_bottom_floor' : 0,
            'w_types' : [TYPE_TENANCY, TYPE_BRF]
        }
        client.post('/create_listing/', data)
        
        listing = Listing.objects.get(o_description='Min')
        listing.delete() # Sets pk to none, but keeps all other data, which should make it identical to the asserted listing
        self.assertEqual(asserted_listing, listing)
        
class ListingModelTests(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user('tester', 'test@example.com', 'password')
        self.other_user = User.objects.create_user('tester2', 'test2@example.com', 'password')
        
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
        listing.o_rooms = 2
        listing.o_street_address = 'Arvid Mörnes väg 42'
        listing.o_type = TYPE_BRF
        listing.w_brf_status = None
        listing.w_county = 'AB'
        listing.w_has_balcony = False
        listing.w_has_elevator = False
        listing.w_has_fireplace = False
        listing.w_max_rent = 5000
        listing.w_min_area = 33
        listing.w_min_rooms = 2
        listing.w_not_bottom_floor = False
        listing.w_types = ','.join([str(TYPE_TENANCY), str(TYPE_BRF)])
        
        listing.user = self.user
        
        self.listing = listing
        self.listing.save()
        
        dummy_listing = Listing()
        dummy_listing.o_area = 33
        dummy_listing.o_brf_status = None
        dummy_listing.o_county = 'AB'
        dummy_listing.o_description = 'Annan'
        dummy_listing.o_floor_no = -1
        dummy_listing.o_has_balcony = 1
        dummy_listing.o_has_elevator = 0
        dummy_listing.o_has_fireplace = 0
        dummy_listing.o_postal_code = '16846'
        dummy_listing.o_rent = 1722
        dummy_listing.o_rooms = 2
        dummy_listing.o_street_address = 'Annan adress'
        dummy_listing.o_type = TYPE_BRF
        dummy_listing.w_brf_status = None
        dummy_listing.w_county = 'AB'
        dummy_listing.w_has_balcony = False
        dummy_listing.w_has_elevator = False
        dummy_listing.w_has_fireplace = False
        dummy_listing.w_max_rent = 5000
        dummy_listing.w_min_area = 33
        dummy_listing.w_min_rooms = 2
        dummy_listing.w_not_bottom_floor = False
        dummy_listing.w_types = ','.join([str(TYPE_TENANCY), str(TYPE_BRF)])
        
        dummy_listing.user = self.other_user
        dummy_listing.save()
        self.dummy_listing = dummy_listing
        
    def tearDown(self):
        self.user.delete()
        self.other_user.delete()
        self.listing.delete()
        self.dummy_listing.delete()
        
    def test_should_match(self):
        matching_listing = self.dummy_listing
        
        self.assertTrue(matching_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_county(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_county = 'W'
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_area(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_area = 32
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_rooms(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_rooms = 1
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_rent(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_rent = 6000
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_type(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_type = TYPE_HOUSE
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_brf_status(self):
        unmatched_listing = self.dummy_listing
        
        unmatched_listing.o_type = TYPE_TENANCY
        unmatched_listing.o_brf_status = BRF_NONE
        unmatched_listing.save()
        
        self.listing.w_brf_status = BRF_FORMED
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_fireplace(self):
        unmatched_listing = self.dummy_listing
        
        self.listing.w_has_fireplace = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_elevator(self):
        unmatched_listing = self.dummy_listing
        
        self.listing.w_has_elevator = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_balcony(self):
        unmatched_listing = self.dummy_listing
        unmatched_listing.o_has_balcony = False
        unmatched_listing.save()
        
        self.listing.w_has_balcony = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_floor(self):
        self.listing.w_not_bottom_floor = True
        self.listing.save()
        
        unmatched_listing = self.dummy_listing
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
        
        
        
        
    
    
