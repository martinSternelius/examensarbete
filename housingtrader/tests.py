# -*- coding: utf-8 -*- 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from housingtrader.models import Listing
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
        
        
    
    
