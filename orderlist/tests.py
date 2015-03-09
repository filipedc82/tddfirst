from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.http import HttpRequest
from orderlist.models import *
from orderlist.views import *
from orderlist.forms import *


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
        self.assertEqual(found.view_name, 'order_detail')

    def test_order_detail_page_returns_correct_html(self):
        order = Order()
        order.order_no='abc123'
        order.save()
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertTemplateUsed(response, 'order_detail.html') #correct template
        self.assertEqual(response.context['order'], order) # correct order in context
        expected_html = render_to_string('order_detail.html', {'order': order})
        self.assertEqual(response.content.decode(), expected_html) # correct html


    def test_order_detail_page_shows_new_order(self):
        order = Order()
        order.order_no = "4711"
        order.customer = "Lego"
        order.save()
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertIn('4711', response.content.decode())
        self.assertIn('Lego', response.content.decode())


class AddOrderPageTest(TestCase):

    def test_add_order_url_resolves_to_add_order_view(self):
        found = resolve('/orders/add/')
        self.assertEqual(found.func, add_order)

    def test_add_order_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        response = add_order(request)
        self.assertTemplateUsed(response, 'add_order.html') #correct template
        expected_html = render_to_string('add_order.html', {'form': OrderForm()})
        self.assertEqual(response.content.decode(), expected_html)

    def test_add_order_page_renders_correct_form(self):
        c = Client()
        response = c.get('/orders/add/')
        self.assertIsInstance(response.context['form'], OrderForm) 	#Sanity-check that your form is rendered, and its errors are displayed.

    def test_add_order_page_can_handle_POST_correct(self):
        c = Client()
        response = c.post('/orders/add/' , {'order_no':'BE0815', 'customer':'A new Customer'})
        self.assertEqual(Order.objects.count(),1)
        new_Order = Order.objects.first()
        self.assertEqual(new_Order.order_no, 'BE0815')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/orders/'+str(new_Order.id)+'/')

    def test_add_order_page_can_handle_POST_incorrect(self):
        c = Client()
        response = c.post('/orders/add/' , {'order_no':'', 'customer':''})
        self.assertEqual(Order.objects.count(),0)
        self.assertEqual(response.status_code, 200)


class OrderListPageTest(TestCase):

    def test_orders_url_resolves_to_order_list_view(self):
        found = resolve('/orders/')
        self.assertEqual(found.view_name, 'order_list')

    def test_order_list_page_returns_correct_html_GET(self):
        c = Client()
        response = c.get('/orders/')
        expected_html = render_to_string('order_list.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_order_list_displays_orders(self):
        first_order = Order()
        first_order.order_no = "FirstOrderNo"
        first_order.customer = "FirstCustomer"
        first_order.save()

        second_order = Order()
        second_order.order_no = "2ndOrderNo"
        second_order.customer = "2ndCustomer"
        second_order.save()

        c = Client()
        response = c.get('/orders/')
        self.assertIn('FirstOrderNo', response.content.decode())
        self.assertIn('2ndCustomer', response.content.decode())



class OrderFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = OrderForm(data={'order': ''})
        self.assertFalse(form.is_valid())

class OrderLineFormTest(TestCase):

    def test_line_form_validation_for_blank_items(self):
        form = OrderLineForm(data={'product': ''})
        self.assertFalse(form.is_valid())

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


