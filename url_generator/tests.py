from unittest import TestCase as BaseTestCase

from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import GeneratedUrls
from .url_generator import get_base_62, generate_url, utilize_url


class UrlGeneratorTest(BaseTestCase):
    def test_get_base_62(self) -> None:
        self.assertEqual(get_base_62(), 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def test_utilize_url(self) -> None:
        urls = [
            ('http://www.google.com', 'google.com'),
            ('http://www.google.com/pkwdowei?w=mdwim&noei', 'google.com/pkwdowei?w=mdwim&noei'),
            ('https://yourgoogle.com/djeiow', 'yourgoogle.com/djeiow'),
        ]
        for url, expected_utilized_url in urls:
            u = utilize_url(url)
            self.assertEqual(u, expected_utilized_url)

    def test_generate_url(self) -> None:
        settings.LENGTH_OF_GENERATED_URL = 7
        generated_urls = [
            ('google.com', 'botCEET'),
            ('google.com/pkwdowei?w=mdwim&noei', 'nvITV7b'),
            ('yourgoogle.com/djeiow', 'lrzNNT5'),
        ]
        for utilized_url, expected_generated_url in generated_urls:
            generated_url = generate_url(utilized_url)
            self.assertEqual(generated_url, expected_generated_url)


class GeneratorOfUrlsCreateViewTest(APITestCase):
    def test_create_new_generated_url_view(self) -> None:
        settings.LENGTH_OF_GENERATED_URL = 7
        response = self.client.post(reverse('url_generator:create-new-url'),
                                    data={'origin_url': 'https://fastapi.tiangolo.com/'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['url'], f'{settings.BASE_URL}/irwwyBE')

        generated_url_obj = GeneratedUrls.objects.filter(alias_url='irwwyBE').first()

        self.assertIsNotNone(generated_url_obj)
        self.assertEqual(generated_url_obj.origin_url, 'fastapi.tiangolo.com/')
        self.assertEqual(generated_url_obj.visited, 0)
        self.assertEqual(generated_url_obj.ip_user, '127.0.0.1')

    def test_create_new_generated_url_view_with_invalid_data(self) -> None:
        settings.LENGTH_OF_GENERATED_URL = 7
        response = self.client.post(reverse('url_generator:create-new-url'),
                                    {'origin_url': '.com/pkwdowei?w=mdwim&noei'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Invalid url!')


class RedirectUrlView(TestCase):
    def test_redirect_to_origin_url_view(self) -> None:
        obj = GeneratedUrls(origin_url='stackoverflow.com', alias_url='stack', visited=5)
        obj.save()

        response = self.client.get(reverse('url_generator:retrieve-origin-url', kwargs={'generated_url': 'stack'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://stackoverflow.com')

        obj.refresh_from_db()
        self.assertEqual(obj.visited, 6)

    def test_redirect_to_origin_url_view_if_url_doesnt_exist(self) -> None:
        response = self.client.get(reverse('url_generator:retrieve-origin-url', kwargs={'generated_url': 'xxxx'}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(b'<h1>Not found url!</h1>', response.content)
