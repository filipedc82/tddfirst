from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from orderlist.models import *
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


class OrderDetailTest(TestCase):

    def test_order_url_resolves_to_order_detail(self):
        found = resolve('/orders/20/')
        self.assertEqual(found.func, order_detail)


    def test_order_detail_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        order = Order()
        order.order_no='abc123'
        order.save()
        response = order_detail(request, order.id)
        expected_html = render_to_string('order_detail.html', {'order': order})
        self.assertEqual(response.content.decode(), expected_html)

class AddOrderPageTest(TestCase):

    def test_add_order_url_resolves_to_add_order_view(self):
        found = resolve('/orders/add/')
        self.assertEqual(found.func, add_order)


    def test_add_order_page_returns_correct_html(self):
        request = HttpRequest()
        response = add_order(request)
        expected_html = render_to_string('add_order.html')
        self.assertEqual(response.content.decode(), expected_html)


class OrderListPageTest(TestCase):

    def test_root_url_resolves_to_order_list_view(self):
        found = resolve('/orders/')
        self.assertEqual(found.func, order_list)

    def test_order_list_page_returns_correct_html_GET(self):
        request = HttpRequest()
        request.method = 'GET'
        response = order_list(request)
        expected_html = render_to_string('order_list.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_order_list_page_can_handle_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['customer']='A new Customer'
        request.POST['order_no']='BE0815'

        response = order_list(request)
        self.assertEqual(Order.objects.count(),1)
        new_Order = Order.objects.first()
        self.assertEqual(new_Order.order_no, 'BE0815')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/orders/'+str(new_Order.id)+'/')

    def test_order_list_displays_orders(self):
        first_order = Order()
        first_order.order_no = "FirstOrderNo"
        first_order.customer = "FirstCustomer"
        first_order.save()

        second_order = Order()
        second_order.order_no = "2ndOrderNo"
        second_order.customer = "2ndCustomer"
        second_order.save()

        request = HttpRequest()
        request.method = 'GET'
        response = order_list(request)
        self.assertIn('FirstOrderNo', response.content.decode())



class ModelTest(TestCase):

    def test_can_save_and_retrieve_Order(self):
        first_order = Order()
        first_order.order_no = "FirstOrderNo"
        first_order.customer = "FirstCustomer"
        first_order.save()

        second_order = Order()
        second_order.order_no = "2ndOrderNo"
        second_order.customer = "2ndCustomer"
        second_order.save()

        saved_orders = Order.objects.all()
        self.assertEqual(saved_orders.count(), 2)

        first_saved_order = saved_orders[0]
        second_saved_order = saved_orders[1]
        self.assertEqual(first_saved_order.order_no, 'FirstOrderNo')
        self.assertEqual(second_saved_order.order_no, '2ndOrderNo')


