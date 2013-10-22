from django.test import TestCase
from registration.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse


class RegistrationViewTests(TestCase):
    
    def test_registration(self):
        client = Client()
        
        username = 'tester'
        password = 'password'
        email = 'tester@example.com'
        first_name = 'John'
        last_name = 'Doe'
        phone_number = '555-12345'
        
        data = {
            'username':username, 
            'email':email, 
            'first_name':first_name, 
            'last_name':last_name, 
            'password1':password, 
            'password2':password,
            'phone_number':phone_number
        }
        
        client.post(reverse('register'), data=data)
        
        asserted_user = User(username=username, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
        actual_user = User.objects.get(username=username)
        self.assertEqual(asserted_user.username, actual_user.username)
        self.assertEqual(asserted_user.email, actual_user.email)
        self.assertEqual(asserted_user.get_full_name(), actual_user.get_full_name())
        self.assertEqual(asserted_user.phone_number, actual_user.phone_number)