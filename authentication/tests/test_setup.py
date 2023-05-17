from rest_framework.test import APITestCase, APIClient
from django.urls import reverse # reverse gives a view name and return us a path to the route. 
from faker import Faker


class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()
        self.user_data = {
            'email': self.fake.email(),
            'password':self.fake.email(),
            'username':self.fake.email().split('@')[0],
        }

        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()