# -*- coding: utf-8 -*- 
from django.test import TestCase
from django.test.client import Client
from registration.models import User
from housingtrader.models import Listing, TradeRequest, TYPE_BRF, TYPE_TENANCY, TYPE_HOUSE, BRF_NONE, BRF_FORMED
from django.core.urlresolvers import reverse

def create_test_users():
    user = User.objects.create_user('tester', 'test@example.com', 'password')
    other_user = User.objects.create_user('tester2', 'test2@example.com', 'password')
    
    return {'user':user, 'other_user':other_user}

def create_test_listings():
    '''
    Creates two Listing objects with the test users of the above function as owners
    '''
    test_users = create_test_users()
    
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
    listing.user = test_users['user']
    listing.save()
    
    other_listing = Listing()
    other_listing.o_area = 33
    other_listing.o_brf_status = None
    other_listing.o_county = 'AB'
    other_listing.o_description = 'Annan'
    other_listing.o_floor_no = -1
    other_listing.o_has_balcony = 1
    other_listing.o_has_elevator = 0
    other_listing.o_has_fireplace = 0
    other_listing.o_postal_code = '16846'
    other_listing.o_rent = 1722
    other_listing.o_rooms = 2
    other_listing.o_street_address = 'Annan adress'
    other_listing.o_type = TYPE_BRF
    other_listing.w_brf_status = None
    other_listing.w_county = 'AB'
    other_listing.w_has_balcony = False
    other_listing.w_has_elevator = False
    other_listing.w_has_fireplace = False
    other_listing.w_max_rent = 5000
    other_listing.w_min_area = 33
    other_listing.w_min_rooms = 2
    other_listing.w_not_bottom_floor = False
    other_listing.w_types = ','.join([str(TYPE_TENANCY), str(TYPE_BRF)])
    other_listing.user = test_users['other_user']
    other_listing.save()
    
    return {'listing':listing, 'other_listing':other_listing}
    

class ListingViewTests(TestCase):
    def setUp(self):
        test_listings = create_test_listings()
        self.listing = test_listings['listing']
        self.other_listing = test_listings['other_listing']
        self.user = test_listings['listing'].user
        self.other_user = test_listings['other_listing'].user
        
    def tearDown(self):
        self.listing.delete()
        self.other_listing.delete()
        self.user.delete()
        self.other_user.delete()
        
    def test_create_listing_view(self):
        '''
        Assertion: A logged in user that sends valid POST data to create_listing will result in a listing correctly saved in the database.
        '''
        listings = Listing.objects.all()
        listings.delete()
        
        client = Client()
        client.login(username='tester', password='password')
        
        o_area = 33
        o_brf_status = ''
        o_county = 'AB'
        o_description = 'Skapa'
        o_floor_no = -1
        o_has_balcony = 1
        o_has_elevator = 1
        o_has_fireplace = 1
        o_postal_code = '16846'
        o_rent = 2001
        o_rooms = 2
        o_street_address = 'Klientvägen 1'
        o_postal_town = 'Stockholm'
        o_type = TYPE_BRF
        w_brf_status = ''
        w_county = 'AB'
        w_has_balcony = 0
        w_has_elevator = 0
        w_has_fireplace = 0
        w_max_rent = 5000
        w_min_area = 90
        w_min_rooms = 2
        w_not_bottom_floor = 0
        w_types = [str(TYPE_TENANCY), str(TYPE_BRF)]
        
        data = {
            'o_area' : o_area,
            'o_brf_status' : o_brf_status,
            'o_county' : o_county,
            'o_description' : o_description,
            'o_floor_no' : o_floor_no,
            'o_has_balcony' : o_has_balcony,
            'o_has_elevator' : o_has_elevator,
            'o_has_fireplace' : o_has_fireplace,
            'o_postal_code' : o_postal_code,
            'o_rent' : o_rent,
            'o_rooms' : o_rooms,
            'o_street_address' : o_street_address,
            'o_postal_town' : o_postal_town,
            'o_type' : o_type,
            'w_brf_status' : w_brf_status,
            'w_county' : w_county,
            'w_max_rent' : w_max_rent,
            'w_min_area' : w_min_area,
            'w_min_rooms' : w_min_rooms,
            'w_not_bottom_floor' : w_not_bottom_floor,
            'w_types' : w_types
        }
        '''
        Note that the fields for balcony, elevator and fireplace are represented by checkboxes. If any value is sent in these keys, even False or None, it will be saved as True.
        Therefore we put no values in the data dictionary for those keys we want to save as False for this test.
        '''
        
        client.post(reverse('housingtrader:create_listing'), data)
        
        '''
        Here we filter listings on every parameter. This is to assert that every parameter gets saved correctly,
        and helps us find on which parameter there is an error, if any.
        '''
        queryset = Listing.objects.filter(o_area = o_area)
        queryset = queryset.filter(o_brf_status = None)
        queryset = queryset.filter(o_county = o_county)
        queryset = queryset.filter(o_description = o_description)
        queryset = queryset.filter(o_floor_no = o_floor_no)
        queryset = queryset.filter(o_has_balcony = o_has_balcony)
        queryset = queryset.filter(o_has_elevator = o_has_elevator)
        queryset = queryset.filter(o_has_fireplace = o_has_fireplace)
        queryset = queryset.filter(o_postal_code = o_postal_code)
        queryset = queryset.filter(o_rent = o_rent)
        queryset = queryset.filter(o_rooms = o_rooms)
        queryset = queryset.filter(o_street_address = o_street_address)
        queryset = queryset.filter(o_postal_town = o_postal_town)
        queryset = queryset.filter(o_type = o_type)
        queryset = queryset.filter(w_brf_status = None)
        queryset = queryset.filter(w_county  =w_county)
        queryset = queryset.filter(w_has_balcony = w_has_balcony)
        queryset = queryset.filter(w_has_elevator = w_has_elevator)
        queryset = queryset.filter(w_has_fireplace = w_has_fireplace)
        queryset = queryset.filter(w_max_rent = w_max_rent)
        queryset = queryset.filter(w_min_area = w_min_area)
        queryset = queryset.filter(w_min_rooms = w_min_rooms)
        queryset = queryset.filter(w_not_bottom_floor = w_not_bottom_floor)
        queryset = queryset.filter(w_types = ','.join(w_types))

        listing = queryset.get()
        
        self.assertTrue(isinstance(listing, Listing))
        self.assertTrue(listing.published)
        
    def test_search(self):
        client = Client()
        
        data = {
            'text' : 'arvid',
            'county' : 'AB',
            'max_rent' : '4000',
            'min_area' : 33,
            'min_rooms' : 1,
            'has_balcony' : 0,
            'has_fireplace' : 0,
            'has_elevator' : 0,
            'not_bottom_floor' : 0,
            'types' : [TYPE_TENANCY, TYPE_BRF],
            'submit' : 1
        }
        
        response = client.get(reverse('housingtrader:search'), data=data)
        self.assertContains(response, text=self.listing.o_street_address)
        self.assertNotContains(response, text=self.other_listing.o_street_address)
        
        data = {
            'text' : 'annan',
            'county' : 'AB',
            'max_rent' : '4000',
            'min_area' : 33,
            'min_rooms' : 1,
            'has_balcony' : 0,
            'has_fireplace' : 0,
            'has_elevator' : 0,
            'not_bottom_floor' : 0,
            'types' : [TYPE_TENANCY, TYPE_BRF],
            'submit' : 1
        }
        
        response = client.get(reverse('housingtrader:search'), data=data)
        self.assertContains(response, text=self.other_listing.o_street_address)
        
        '''
        Assert that a search can be performed with empty text field
        '''
        data = {
            'text' : '   ',
            'county' : 'AB',
            'max_rent' : 4000,
            'min_area' : 33,
            'min_rooms' : 1,
            'has_balcony' : 0,
            'has_fireplace' : 0,
            'has_elevator' : 0,
            'not_bottom_floor' : 0,
            'types' : [TYPE_TENANCY, TYPE_BRF],
            'submit' : 1
        }
        
        response = client.get(reverse('housingtrader:search'), data=data)
        self.assertContains(response, text=self.listing.o_street_address)
        self.assertContains(response, text=self.other_listing.o_street_address)
        
        '''
        Assert that an unpublished listing does not show up in a search
        '''
        self.listing.change_published_state()
        data = {
            'text' : '   ',
            'county' : 'AB',
            'max_rent' : 4000,
            'min_area' : 33,
            'min_rooms' : 1,
            'has_balcony' : 0,
            'has_fireplace' : 0,
            'has_elevator' : 0,
            'not_bottom_floor' : 0,
            'types' : [TYPE_TENANCY, TYPE_BRF],
            'submit' : 1
        }
        
        response = client.get(reverse('housingtrader:search'), data=data)
        self.assertNotContains(response, text=self.listing.o_street_address)
        
        
    def test_change_published_state(self):
        client = Client()
        client.login(username=self.user.username, password='password')
        client.post(reverse('housingtrader:change_published_state', args=[self.listing.pk]))
        
        listing_after_unpublish = Listing.objects.get(pk=self.listing.pk)
        self.assertFalse(listing_after_unpublish.published)
        
class ListingFindMatchesTests(TestCase):
    def setUp(self):
        test_listings = create_test_listings()
        
        self.listing = test_listings['listing']
        self.user = self.listing.user
        
        self.other_listing = test_listings['other_listing']
        self.other_user = self.other_listing.user
        
    def tearDown(self):
        self.user.delete()
        self.other_user.delete()
        self.listing.delete()
        self.other_listing.delete()
        
    def test_should_match(self):
        matching_listing = self.other_listing
        
        self.assertTrue(matching_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_county(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_county = 'W'
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_area(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_area = 32
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_rooms(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_rooms = 1
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_rent(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_rent = 6000
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_type(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_type = TYPE_HOUSE
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_brf_status(self):
        unmatched_listing = self.other_listing
        
        unmatched_listing.o_type = TYPE_TENANCY
        unmatched_listing.o_brf_status = BRF_NONE
        unmatched_listing.save()
        
        self.listing.w_brf_status = BRF_FORMED
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_fireplace(self):
        unmatched_listing = self.other_listing
        
        self.listing.w_has_fireplace = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_elevator(self):
        unmatched_listing = self.other_listing
        
        self.listing.w_has_elevator = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_balcony(self):
        unmatched_listing = self.other_listing
        unmatched_listing.o_has_balcony = False
        unmatched_listing.save()
        
        self.listing.w_has_balcony = True
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_floor(self):
        self.listing.w_not_bottom_floor = True
        self.listing.save()
        
        unmatched_listing = self.other_listing
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_same_user(self):
        unmatched_listing = self.other_listing
        unmatched_listing.user = self.user
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_should_not_match_because_of_unpublished(self):
        unmatched_listing = self.other_listing
        unmatched_listing.change_published_state()
        
        self.assertFalse(unmatched_listing in self.listing.find_matches())
        
    def test_reverse_should_match(self):
        matched_listing = self.other_listing
        self.assertTrue(matched_listing in self.listing.find_reverse_matches())
    

    def test_reverse_should_not_match_because_of_county(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_county = 'F'
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_area(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_min_area = 34
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_rooms(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_min_rooms = 3
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_rent(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_max_rent = 1700
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_type(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_types = [TYPE_HOUSE]
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_brf_status(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_brf_status = BRF_FORMED
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_fireplace(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_has_fireplace = True
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_elevator(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_has_elevator = True
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_balcony(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_has_balcony = True
        unmatched_listing.save()
        
        self.listing.o_has_balcony = False
        self.listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_floor(self):
        unmatched_listing = self.other_listing
        unmatched_listing.w_not_bottom_floor = True
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_same_user(self):
        unmatched_listing = self.other_listing
        unmatched_listing.user = self.user
        unmatched_listing.save()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_reverse_should_not_match_because_of_unpublished(self):
        unmatched_listing = self.other_listing
        unmatched_listing.change_published_state()
        
        self.assertFalse(unmatched_listing in self.listing.find_reverse_matches())
        
    def test_mutual_match(self):
        matched_listing = self.other_listing
        
        self.assertTrue(matched_listing in self.listing.find_mutual_matches())
        
        
class TradeRequestModelTests(TestCase):
    
    def setUp(self):
        test_listings = create_test_listings()
        self.listing = test_listings['listing']
        self.other_listing = test_listings['other_listing']
        
    def tearDown(self):
        self.listing.delete()
        self.other_listing.delete()
        self.listing.user.delete()
        self.other_listing.user.delete()
    
    def test_trade_request_save(self):
        trade_request = TradeRequest(requester=self.listing, receiver=self.other_listing)
        trade_request.save()
        
        trade_request1 = self.listing.trade_requests_sent.get(receiver=self.other_listing)
        trade_request2 = self.other_listing.trade_requests_received.get(requester=self.listing)
        
        self.assertEqual(trade_request1.pk, trade_request2.pk)
        
        
    
    
