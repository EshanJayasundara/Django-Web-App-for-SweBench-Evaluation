# swe_api/tests.py

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework_api_key.models import APIKey

class SampleAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a real API Key for testing
        self.api_key_obj, self.api_key = APIKey.objects.create_key(name="test-api-key")
        self.url = reverse('test')

    def test_admin_status_code(self):
        # Add correct Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key}')
        response = self.client.get(self.url)
        # Check for success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data'], "Successfully, you reached the 'test' endpoint authenticated with an API-Key.")
