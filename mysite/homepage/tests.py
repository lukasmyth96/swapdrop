from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):

    def setUp(self) -> None:
        url = reverse('landing-page')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

