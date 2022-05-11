from django.test import TestCase
from .models import ShortURL
from django.urls import reverse
from . import utils
from django.db import IntegrityError
from django.http import HttpRequest
from http import HTTPStatus

# Create your tests here.


# function for creating instance of ShortURL model
def create_short_url(full_url, number_of_uses):
    return ShortURL.objects.create(
        hashed_url=utils.hash_url(full_url),
        full_url=full_url,
        number_of_uses=number_of_uses)


# class for testing ShortURL model
class ShortURLModelTests(TestCase):

    def test_hashed_url_max_length(self):
        
        max_length = 8
        
        # create instance of ShortURL model
        short_url = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # assert that length of hashed url is equal max_length(8)
        self.assertEqual(len(short_url.hashed_url), max_length)

    
    def test_full_url_uniqueness(self):

        # create instance №1 of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # assert that trying to create short_url_2 with same full_url as short_url_1 raises error
        with self.assertRaises(IntegrityError):
            short_url_2 = create_short_url(
                full_url="https://www.example.com/", 
                number_of_uses=10)

    
    def test_hashed_url_uniqueness(self):

        # create instance №1 of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # create instance №2 of ShortURL model
        short_url_2 = create_short_url(
            full_url="https://www.instance.com/", 
            number_of_uses=10)

        # assert that trying to change short_url_2 with same hashed_url as short_url_1 raises error
        with self.assertRaises(IntegrityError):
            short_url_2.hashed_url = short_url_1.hashed_url
            short_url_2.save()


    def test_number_of_uses_negative_value(self):

        # assert that creating instance of ShortURL model with negative value of number_of_uses raises error
        with self.assertRaises(IntegrityError):
            short_url = create_short_url(
                full_url="https://www.example.com/", 
                number_of_uses=-5)


# class for testing index view
class IndexViewTests(TestCase):

    def test_index_view(self):

        # get response by url to index view
        response = self.client.get(reverse('url_shortener:index'))

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # assert that response contains link to All Links page
        self.assertContains(response, 'All Links')

        # assert that response contains input for full urls
        self.assertContains(response, 
            'Enter a long URL to make a ShortURL')

        # assert that response contains button with value 'Make ShortURL!'
        self.assertContains(response, 'Make ShortURL!')


    def test_create_short_url_view(self):
        
        # create full_url for example
        full_url = 'https://www.youtube.com/'

        # get response by url to create_short_url view
        response = self.client.post('/myurl', data={"input-url": full_url})

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # get object from db after view work
        short_url_object = ShortURL.objects.get(full_url=full_url)

        # assert that full url of short_url from db is equal to full_url
        self.assertEqual(short_url_object.full_url, full_url)

        # assert that number of uses of short_url from db is equal to 0, because it is new object
        self.assertEqual(short_url_object.number_of_uses, 0)

        # assert that response contains hashed_url of created short_url from db 
        self.assertContains(response, short_url_object.hashed_url)


# class for testing AllLinksView  
class AllLinksViewTests(TestCase):

    def test_no_short_urls(self):

        # get response by url to all_links view
        response = self.client.get(reverse('url_shortener:all_links'))

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # assert that response does not contain short urls, cause we haven't created ones
        self.assertContains(response, 'No short urls available')

        # assert that response does not contain context object (list) of short url from db
        self.assertQuerysetEqual(response.context['short_urls'], [])

    
    def test_with_short_urls(self):

        # create instance №1 of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # create instance №2 of ShortURL model
        short_url_2 = create_short_url(
            full_url="https://www.instance.com/", 
            number_of_uses=10)

        # create instance №3 of ShortURL model
        short_url_3 = create_short_url(
            full_url="https://www.sample.com/", 
            number_of_uses=7)

        # create list of created short_urls
        lst_of_short_urls = [short_url_1 ,short_url_2, short_url_3]

        # sort list by number_of_uses in reverse mod to test ordering in view 
        lst_of_short_urls.sort(key=lambda x: x.number_of_uses, reverse=True)

        # get response by url to all_links view
        response = self.client.get(reverse('url_shortener:all_links'))

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # assert that response contains some short urls, cause we have created ones
        self.assertNotContains(response, 'No short urls available')

        # assert that response contains list of short_urls in right order
        self.assertQuerysetEqual(response.context['short_urls'], lst_of_short_urls)


    def test_delete_short_url(self):

        # create instance of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # get response by url to all_links view
        response = self.client.get(reverse('url_shortener:all_links'))

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # assert that response contains some short urls, cause we have created one
        self.assertNotContains(response, 'No short urls available')

        # assert that response contains list with short_url_1
        self.assertQuerysetEqual(response.context['short_urls'], [short_url_1])

        # make request by url to delete_short_url view to delete short_url from db
        self.client.delete(reverse('url_shortener:delete', args=(short_url_1.id, )))

        # get response by url to all_links view
        response_2 = self.client.get(reverse('url_shortener:all_links'))

        # assert that status code of response is equal HTTPStatus.OK(OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # assert that response does not contain some short url, because we have deleted one
        self.assertContains(response_2, 'No short urls available')

        # assert that response does not contain list with short_url_1
        self.assertQuerysetEqual(response_2.context['short_urls'], [])


    def test_delete_non_existent_short_url(self):

        # create instance of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.example.com/", 
            number_of_uses=5)

        # make request by url to delete_short_url view to delete short_url from db
        response_1 = self.client.delete(reverse('url_shortener:delete', args=(short_url_1.id, )))

        # make request by url to delete_short_url view to delete non-existent short_url
        response_2 = self.client.delete(reverse('url_shortener:delete', args=(short_url_1.id, )))

        # assert that status code of response is equal to 404 (Not found)
        self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)


# class for testing handle_short_url view
class HandleShortURLTests(TestCase):

    def test_handle_short_url(self):
        # create instance of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.youtube.com/", 
            number_of_uses=5)

        # get response by url to handle_short_url view
        response = self.client.get(reverse('url_shortener:handle', args=(short_url_1.hashed_url, )))
        
        # assert that response's url is equal to full url
        self.assertEqual(response.url, 'https://www.youtube.com/')


    def test_handle_short_url_increase_number_of_uses(self):

        test_number_of_uses = 5

        # create instance of ShortURL model
        short_url_1 = create_short_url(
            full_url="https://www.youtube.com/", 
            number_of_uses=test_number_of_uses)

        # get response by url to handle_short_url view
        self.client.get(reverse('url_shortener:handle', args=(short_url_1.hashed_url, )))

        # assert that number of uses of this short url is increased by 1
        self.assertNotEqual(ShortURL.objects.get(pk=short_url_1.id).number_of_uses, test_number_of_uses)
        self.assertEqual(ShortURL.objects.get(pk=short_url_1.id).number_of_uses, test_number_of_uses + 1)


# class for testing functions from utils.py
class UtilsFunctionsTests(TestCase):

    def test_is_valid_url(self):

        # creating different instances of urls and not url
        right_url = "https://www.example.com/"
        wrong_url = "httpsS://www.sample.com/"
        not_url = "instance"

        # assert that right_url has right url format
        self.assertIs(utils.is_valid_url(right_url), True)

        # assert that wrong_url has wrong url format
        self.assertIs(utils.is_valid_url(wrong_url), False)

        # assert that not_url is not url at all
        self.assertIs(utils.is_valid_url(not_url), False)


    def test_hash_url(self):

        url = "https://www.example.com/"

        # creating several hashed of the same url 
        hash_url_1 = utils.hash_url(url)
        hash_url_2 = utils.hash_url(url)

        # assert that we get only first 8 symbols of hash
        self.assertEqual(len(hash_url_1), 8)

        # assert that even hashes of the same url are different
        self.assertNotEqual(hash_url_1, hash_url_2)