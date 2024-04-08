# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_registration_without_referral_code(self):
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)

    def test_successful_registration_with_referral_code(self):
        referrer = User.objects.create_user(username='referrer', email='referrer@example.com', password='password')
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword', 'referral_code': referrer.profile.referral_code}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user_id', response.data)
        self.assertEqual(referrer.profile.points, 1)

    def test_registration_with_missing_required_field(self):
        data = {'name': 'Test User', 'password': 'testpassword'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_duplicate_email(self):
        User.objects.create_user(username='existing_user', email='test@example.com', password='password')
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_successful_retrieval_of_user_details(self):
        response = self.client.get('/api/user-details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertIn('email', response.data)
        self.assertIn('referral_code', response.data)

    def test_retrieval_with_invalid_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/user-details/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReferralsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='referrer', email='referrer@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    def test_successful_retrieval_of_referrals(self):
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions for the structure of the response if needed

    def test_retrieval_of_referrals_with_no_referrals(self):
        # No additional setup needed, as the referrer has no referrals yet
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieval_with_invalid_token(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/referrals/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Additional tests for general security vulnerabilities can be added here
