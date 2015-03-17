from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.http import HttpRequest
from orderlist.models import *
from orderlist.views import *
from orderlist.forms import *


def createTestOrder():
    order = Order()
    order.order_no = str(Order.objects.count()+4811)
    order.customer = "Lego"
    order.save()
    return order

def createTestOrderLine(my_order):
    ol = OrderLine()
    ol.order = my_order
    ol.dlry_date = '2015-05-05'
    ol.product = 'anotherGuide'
    ol.unit_price = 10.0 + OrderLine.objects.count()
    ol.qty = 200 + OrderLine.objects.count()
    ol.save()
    return ol

def createTestDelivery():
    dlry = Delivery()
    dlry.dlry_no = str(Delivery.objects.count()+815)
    dlry.recipient = "Lego"
    dlry.sender = "DCA"
    dlry.dispatch_date = "2015-04-05"
    dlry.save()
    print(str(dlry.dlry_no))
    return dlry

def createTestDeliveryLine(my_dlry):
    dl = DeliveryLine()
    dl.delivery = my_dlry
    dl.product = 'anotherGuide'
    dl.qty = 150
    ol = createTestOrderLine(createTestOrder())
    dl.order_line = ol
    dl.save()
    return dl

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

class DeliveryListPageTest(TestCase):

    def test_deliveries_url_resolves_to_deliveries_list_view(self):
        found = resolve('/deliveries/')
        self.assertEqual(found.view_name, 'delivery_list')

    def test_delivery_list_page_returns_correct_html_GET(self):
        c = Client()
        response = c.get('/deliveries/')
        expected_html = render_to_string('delivery_list.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_order_list_displays_orders(self):
        createTestDelivery()
        createTestDelivery()
        c = Client()
        response = c.get('/deliveries/')
        self.assertIn('Lego', response.content.decode())
        self.assertIn('DCA', response.content.decode())
        self.assertIn('815', response.content.decode())
        self.assertIn('816', response.content.decode())

class DeliveryDetailTest(TestCase):

    def test_delivery_url_resolves_to_delivery_detail(self):
        found = resolve('/deliveries/20/')
        self.assertEqual(found.view_name, 'delivery_detail')

    def test_delivery_detail_page_returns_correct_html(self):
        delivery = createTestDelivery()
        c = Client()
        response = c.get('/deliveries/'+str(delivery.id)+'/')
        self.assertTemplateUsed(response, 'delivery_detail.html') #correct template
        self.assertEqual(response.context['delivery'], delivery) # correct delivery in context
        expected_html = render_to_string('delivery_detail.html', {'delivery': delivery})
        #self.assertEqual(response.content.decode(), expected_html) # correct html

    def test_delivery_detail_page_shows_new_delivery(self):
        delivery = createTestDelivery()
        c = Client()
        response = c.get('/deliveries/'+str(delivery.id)+'/')
        self.assertIn('DCA', response.content.decode())
        self.assertIn('Lego', response.content.decode())

    def test_delivery_detail_page_shows_delivery_line(self):
        delivery = createTestDelivery()
        dl = createTestDeliveryLine(delivery)
        c = Client()
        response = c.get('/deliveries/'+str(delivery.id)+'/')
        self.assertIn(dl.product, response.content.decode())
        self.assertIn(dl.order_line.order.order_no, response.content.decode())

class DeliveryAddPageTest(TestCase):

    def test_add_delivery_url_resolves_to_add_delivery_view(self):
        found = resolve('/deliveries/add/1,2,')
        self.assertEqual(found.func, add_delivery)




class DeliverySelectOLPageTest(TestCase):

    def test_select_ol_url_resolves_to_select_ol_view(self):
        found = resolve('/deliveries/add/')
        self.assertEqual(found.func, select_ol)

    def test_select_ol_page_returns_correct_html(self):
        c = Client()
        o = createTestOrder()
        ol = createTestOrderLine(o)
        ol_select_form = OrderLineSelectForm({'orderLine': ol})
        response = c.get('/deliveries/add/')
        self.assertTemplateUsed(response, 'select_ol.html')  # correct template
        # expected_html = render_to_string('select_ol.html'})
        #self.assertEqual(response.content.decode(), expected_html)

    def test_select_ol_page_renders_correct_order_line_select_forms(self):
        order = createTestOrder()
        ol = createTestOrderLine(order)
        c = Client()
        response = c.get('/deliveries/add/')
        olsformcandidate= response.context['order_line_select_forms'][0]
        self.assertIs(type(olsformcandidate), OrderLineSelectForm) 	#Sanity-check that your form is rendered
        self.assertIn(order.order_no, response.content.decode())
        self.assertIn(ol.product, response.content.decode())



    def test_select_ol_view_creates_correct_get_url(self):
        order = createTestOrder()
        ol = createTestOrderLine(order)
        ol2 = createTestOrderLine(order)
        ol3 = createTestOrderLine(order)
        c = Client()
        response = c.post('/deliveries/add/', {
                     'form-0-order_line_id': ol.id,
                     'form-0-order_qty': ol.qty,
                     'form-0-order_no':ol.order.order_no,
                     'form-0-product': ol.product,
                     'form-0-customer': ol.order.customer,
                     'form-0-selected': True,
                     'form-1-order_line_id': ol2.id,
                     'form-1-order_qty': ol2.qty,
                     'form-1-order_no':ol2.order.order_no,
                     'form-1-product': ol2.product,
                     'form-1-customer': ol2.order.customer,
                     'form-1-selected': True,
                     'form-2-order_line_id': ol3.id,
                     'form-2-order_qty': ol3.qty,
                     'form-2-order_no':ol3.order.order_no,
                     'form-2-product': ol3.product,
                     'form-2-customer': ol3.order.customer,
                     })
        self.assertRedirects(response, '/deliveries/add/'+str(ol.id)+','+str(ol2.id)+',')
        #todo: finish

class OrderDetailTest(TestCase):

    def test_order_url_resolves_to_order_detail(self):
        found = resolve('/orders/20/')
        self.assertEqual(found.view_name, 'order_detail')

    def test_order_detail_page_returns_correct_html(self):
        order = createTestOrder()
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertTemplateUsed(response, 'order_detail.html') #correct template
        self.assertEqual(response.context['order'], order) # correct order in context
        expected_html = render_to_string('order_detail.html', {'order': order, 'orderLineform':OrderLineForm()})
        #TODO: self.assertEqual(response.content.decode(), expected_html) # correct html

    def test_order_detail_page_shows_new_order(self):
        order = createTestOrder()
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertIn('4811', response.content.decode())
        self.assertIn('Lego', response.content.decode())

    def test_order_detail_page_shows_order_line(self):
        order = createTestOrder()
        ol = createTestOrderLine(order)
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertIn('anotherGuide', response.content.decode())

    def test_order_detail_page_renders_correct_form(self):
        order = createTestOrder()
        c = Client()
        response = c.get('/orders/'+str(order.id)+'/')
        self.assertIsInstance(response.context['orderLineForm'], OrderLineForm) 	#Sanity-check that your form is rendered, and its errors are displayed.

    def test_order_detail_page_can_handle_POST_correct(self):
        order = createTestOrder()
        c = Client()
        response = c.post('/orders/'+str(order.id)+'/', {'order': order.id, 'product':'aGuide', 'qty': 10.0, 'unit_price': 15.0, 'dlry_date':'2015-05-05'})
        self.assertEqual(OrderLine.objects.count(),1)
        new_Order_Line = OrderLine.objects.first()
        self.assertEqual(new_Order_Line.product, 'aGuide')
        self.assertEqual(new_Order_Line.order_id, order.id)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/orders/'+str(order.id)+'/')

    def test_add_order_page_can_handle_POST_incorrect(self):
        order = createTestOrder()
        c = Client()
        response = c.post('/orders/'+str(order.id)+'/', {'order': order.id, 'product':'', 'qty':'', 'unit_price': '', 'dlry_date':''})
        self.assertEqual(OrderLine.objects.count(),0)
        self.assertEqual(response.status_code, 200)

class OrderAddPageTest(TestCase):

    def test_add_order_url_resolves_to_add_order_view(self):
        found = resolve('/orders/add/')
        self.assertEqual(found.func, add_order)

    def test_add_order_page_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        response = add_order(request)
        #c = Client()
        #response = c.get('/orders/add/')
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


#class OrderLineSelectFormTest(TestCase):
#todo: How to test this form?
    # def test_line_form_validation_for_blank_items(self):
    #     form = OrderLineForm(data={'product': ''})
    #     self.assertFalse(form.is_valid())





class ModelTest(TestCase):

    def test_can_save_and_retrieve_Order_and_OrderLine(self):
        first_order = Order()
        first_order.order_no = "FirstOrderNo"
        first_order.customer = "FirstCustomer"
        first_order.save()

        second_order = Order()
        second_order.order_no = "2ndOrderNo"
        second_order.customer = "2ndCustomer"
        second_order.save()
        oL = OrderLine()
        oL.order_id = second_order.id
        oL.unit_price = 10.5
        oL.product = 'aGuide'
        oL.dlry_date = '2014-05-05'
        oL.qty = 25.5
        oL.save()

        saved_orders = Order.objects.all()
        self.assertEqual(saved_orders.count(), 2)
        self.assertEqual(OrderLine.objects.all().count(),1)

        first_saved_order = saved_orders[0]
        second_saved_order = saved_orders[1]
        self.assertEqual(first_saved_order.order_no, 'FirstOrderNo')
        self.assertEqual(second_saved_order.order_no, '2ndOrderNo')
        self.assertEqual(second_saved_order.orderline_set.count(), 1)
        self.assertEqual(second_saved_order.orderline_set.last().product, 'aGuide')

