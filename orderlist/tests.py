from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from orderlist.views import *


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


    def test_add_order_url_resolves_to_add_order_view(self):
        found = resolve('/orders/add')
        self.assertEqual(found.func, add_order)


    def test_add_order_page_returns_correct_html(self):
        request = HttpRequest()
        response = add_order(request)
        expected_html = render_to_string('add_order.html')
        self.assertEqual(response.content.decode(), expected_html)