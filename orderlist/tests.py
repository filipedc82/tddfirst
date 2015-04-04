from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.http import HttpRequest
from orderlist.models import *
from orderlist.views import *
from orderlist.forms import *

## HELPERS
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
    ol.product = 'anotherGuide'+str(OrderLine.objects.count())
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

def createTestInvoice():
    i = Invoice()
    i.debitor = "MWH"
    i.invoice_date = "2015-04-04"
    i.invoice_no = "Invoice"+str(Invoice.objects.count())
    i.save()
    return i


def createTestInvoiceLine(my_invoice):
    il = InvoiceLine()
    il.invoice = my_invoice
    il.product = 'anotherGuide'
    il.qty = 150
    ol = createTestOrderLine(createTestOrder())
    il.order_line = ol
    il.unit_price = ol.unit_price - 1
    dl = createTestDeliveryLine(createTestDelivery())
    il.delivery_line = dl
    il.save()
    return il


## PAGE and VIEW TESTS
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class InvoiceListPageTest(TestCase):

    def test_invoices_url_resolves_to_invoices_list_view(self):
        found = resolve('/invoices/')
        self.assertEqual(found.view_name, 'invoice_list')

    def test_invoice_list_page_returns_correct_html_GET(self):
        c = Client()
        response = c.get('/invoices/')
        expected_html = render_to_string('invoice_list.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_invoice_list_displays_invoices(self):
        createTestInvoice()
        createTestInvoice()
        c = Client()
        response = c.get('/invoices/')
        self.assertIn('MWH', response.content.decode())
        self.assertIn('Invoice0', response.content.decode())
        self.assertIn('Invoice1', response.content.decode())

class InvoiceDetailTest(TestCase):

    def test_invoice_url_resolves_to_invoice_detail(self):
        found = resolve('/invoices/20/')
        self.assertEqual(found.view_name, 'invoice_detail')

    def test_invoice_detail_page_returns_correct_html(self):
        invoice = createTestInvoice()
        c = Client()
        response = c.get('/invoices/'+str(invoice.id)+'/')
        self.assertTemplateUsed(response, 'invoice_detail.html') #correct template
        self.assertEqual(response.context['invoice'], invoice) # correct invoice in context
        expected_html = render_to_string('invoice_detail.html', {'invoice': invoice})
#        self.assertEqual(response.content.decode(), expected_html) # correct html

    def test_invoice_detail_page_shows_new_invoice(self):
        invoice = createTestInvoice()
        c = Client()
        response = c.get('/invoices/'+str(invoice.id)+'/')
        self.assertIn(invoice.invoice_no, response.content.decode())
        self.assertIn(invoice.debitor, response.content.decode())
        self.assertIn(invoice.get_invoice_value(), response.content.decode())

    def test_invoice_detail_page_shows_invoice_line(self):
        invoice = createTestInvoice()
        il = createTestInvoiceLine(invoice)
        c = Client()
        response = c.get('/invoices/'+str(invoice.id)+'/')
        self.assertIn(il.product, response.content.decode())
        self.assertIn(il.order_line.order.order_no, response.content.decode())

class InvoiceSelectDLPageTest(TestCase):

    def test_select_dl_url_resolves_to_select_ol_view(self):
        found = resolve('/invoices/add/')
        self.assertEqual(found.func, select_dl)

    def test_select_dl_page_returns_correct_html_template(self):
        c = Client()
        response = c.get('/invoices/add/')
        self.assertTemplateUsed(response, 'select_dl.html')  # correct template

    def test_select_dl_page_renders_correct_delivery_line_select_forms(self):
        delivery = createTestDelivery()
        dl = createTestDeliveryLine(delivery)
        c = Client()
        response = c.get('/invoices/add/')
        dlsformcandidate= response.context['delivery_line_select_forms'][0]
        self.assertIs(type(dlsformcandidate), DeliveryLineSelectForm) 	#Sanity-check that your form is rendered
        self.assertIn(delivery.dlry_no, response.content.decode())
        self.assertIn(dl.product, response.content.decode())



class DeliveryListPageTest(TestCase):

    def test_deliveries_url_resolves_to_deliveries_list_view(self):
        found = resolve('/deliveries/')
        self.assertEqual(found.view_name, 'delivery_list')

    def test_delivery_list_page_returns_correct_html_GET(self):
        c = Client()
        response = c.get('/deliveries/')
        expected_html = render_to_string('delivery_list.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_delivery_list_displays_deliveries(self):
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

    def test_add_delivery_url_returns_correct_html(self):
        d = createTestDelivery()
        dl = createTestDeliveryLine(d)
        o = createTestOrder()
        ol1 = createTestOrderLine(o)
        ol2 = createTestOrderLine(o)
        response = Client().get('/deliveries/add/1,2,')
        self.assertTemplateUsed(response, 'add_delivery.html')  # correct template

    def test_add_delivery_page_renders_correct_forms(self):
        o = createTestOrder()
        ol1 = createTestOrderLine(o)
        ol2 = createTestOrderLine(o)
        c = Client()
        response = c.get('/deliveries/add/2,1,')
        self.assertIsInstance(response.context['dform'], DeliveryForm) 	#Sanity-check that your form is rendered, and its errors are displayed.
        dlformcandidate= response.context['dlforms'][0]
        self.assertIs(type(dlformcandidate), DeliveryLineForm) 	#Sanity-check that your form is rendered



    def test_add_delivery_page_can_handle_POST_correct(self):
        o = createTestOrder()
        ol1 = createTestOrderLine(o)
        ol2 = createTestOrderLine(o)
        c = Client()
        response = c.post('/deliveries/add/2,1,' , {'dlry_no':'DLRY666',
                                                    'recipient':'myRecepient',
                                                    'sender':'mySender',
                                                    'dispatch_date':'2015-1-1',
                                                    'form-TOTAL_FORMS': '4',
                                                    'form-INITIAL_FORMS': '2',
                                                    'form-MAX_NUM_FORMS': '1000',
                                                    'form-0-product': str(ol1.product),
                                                    'form-0-qty': str(ol1.qty-5),
                                                    'form-0-order_no':(ol1.order.order_no),
                                                    'form-0-order_line': str(ol1.id),
                                                    'form-1-product':str(ol2.product),
                                                    'form-1-qty':str(ol2.qty),
                                                    'form-1-order_no':str(ol2.order.order_no),
                                                    'form-1-order_line': str(ol2.id),
                                                    'form-2-product':'thirdGuide',
                                                    'form-2-qty':'1000',
                                                    'form-2-order_no':'',
                                                    'form-2-order_line':'',
                                                    'form-3-product':'',
                                                    'form-3-qty':'',
                                                    'form-3-order_no':'',
                                                    'form-3-order_line':'',
                                                    })
        self.assertEqual(Delivery.objects.count(),1)
        new_Delivery = Delivery.objects.first()
        self.assertEqual(new_Delivery.dlry_no, 'DLRY666')
        self.assertEqual(DeliveryLine.objects.count(), 3)
        self.assertEqual(DeliveryLine.objects.filter(delivery=new_Delivery).count(), 3)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,'/deliveries/'+str(new_Delivery.id)+'/')

    def test_add_delivery_page_can_handle_POST_incorrect(self):
        o = createTestOrder()
        ol1 = createTestOrderLine(o)
        ol2 = createTestOrderLine(o)
        c = Client()
        response = c.post('/deliveries/add/2,1,', {'form-TOTAL_FORMS': '4', 'form-INITIAL_FORMS': '2', 'form-MAX_NUM_FORMS': '5'})
        self.assertEqual(Delivery.objects.count(),0)
        self.assertEqual(DeliveryLine.objects.count(),0)
        self.assertEqual(response.status_code, 200)

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
                     'form-0-selected': 'on',
                     'form-1-order_line_id': ol2.id,
                     'form-1-order_qty': ol2.qty,
                     'form-1-order_no':ol2.order.order_no,
                     'form-1-product': ol2.product,
                     'form-1-customer': ol2.order.customer,
                     'form-1-selected': 'on',
                     'form-2-order_line_id': ol3.id,
                     'form-2-order_qty': ol3.qty,
                     'form-2-order_no':ol3.order.order_no,
                     'form-2-product': ol3.product,
                     'form-2-customer': ol3.order.customer,
                     'form-2-selected': 'off',
                     })
        self.assertIn(str(ol.id),str(response.url))
        self.assertIn(str(ol2.id),str(response.url))
        self.assertIn("/deliveries/add/",str(response.url))


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



## TESTS FOR FORMS
class OrderFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = OrderForm(data={'order': ''})
        self.assertFalse(form.is_valid())

class OrderLineFormTest(TestCase):

    def test_line_form_validation_for_blank_items(self):
        form = OrderLineForm(data={'product': ''})
        self.assertFalse(form.is_valid())

class OrderLineSelectFormTest(TestCase):

    def test_line_form_validation_for_blank_items(self):
        form = OrderLineSelectForm(data={'product': ''})
        self.assertFalse(form.is_valid())

    def test_ol_select_form_elements_ro_except_select(self):
        o = createTestOrder()
        ol = createTestOrderLine(o)
        oldata = {  'order_line_id': ol.id,
                    'order_qty': ol.qty,
                    'order_no':ol.order.order_no,
                    'product': ol.product,
                    'customer': ol.order.customer,
                    }
        olsform = OrderLineSelectForm(oldata)
        self.assertTrue(olsform.fields['product'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(olsform.fields['order_no'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(olsform.fields['order_qty'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(olsform.fields['customer'].widget.attrs.get("class")=="form-control-static")
        self.assertIsInstance(olsform.fields['order_line_id'].widget, widgets.HiddenInput)
        self.assertIsInstance(olsform.fields['selected'], BooleanField)



class DeliveryFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = DeliveryForm(data={})
        self.assertFalse(form.is_valid())

class DeliveryLineFormTest(TestCase):
    def test_form_validation_for_blank_items(self):
        form = DeliveryLineForm(data={})
        self.assertFalse(form.is_valid())

    def test_dl_formset(self):
        ol = createTestOrderLine(createTestOrder())
        ol2 = createTestOrderLine(createTestOrder())
        dlformset = formset_factory(DeliveryLineForm, extra=2)

        data = {'dlry_no':'DLRY666',
                'recipient':'myRecepient',
                'sender':'mySender',
                'dispatch_date':'2015-1-1',
                'form-TOTAL_FORMS': '4',
                'form-INITIAL_FORMS': '2',
                'form-MAX_NUM_FORMS': '1000',
                'form-0-product':'anotherGuide1',
                'form-0-qty':'201',
                'form-0-order_no':'4811',
                'form-0-order_line':'1',
                'form-1-product':'anotherGuide0',
                'form-1-qty':'200',
                'form-1-order_no':'4811',
                'form-1-order_line':'1',
                'form-2-product':'thirdGuide',
                'form-2-qty':'1000',
                'form-2-order_no':'',
                'form-3-product':'',
                'form-3-qty':'',
                'form-3-order_no':'',
                'form-3-order_line':'',
                }

        dlforms = dlformset(data)
        self.assertTrue(dlforms.is_valid())

class DeliveryLineSelectFormTest(TestCase):

    def test_line_form_validation_for_blank_items(self):
        form = DeliveryLineSelectForm(data={'product': ''})
        self.assertFalse(form.is_valid())

    def test_dl_select_form_elements_ro_except_select(self):
        d = createTestDelivery()
        dl = createTestDeliveryLine(d)
        dldata = {  'delivery_line_id': dl.id,
                    'qty': dl.qty,
                    'delivery_no':dl.delivery.dlry_no,
                    'product': dl.product,
                    'recipient': dl.delivery.recipient,
                    }
        dlsform = DeliveryLineSelectForm(dldata)
        self.assertTrue(dlsform.fields['delivery_no'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(dlsform.fields['product'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(dlsform.fields['qty'].widget.attrs.get("class")=="form-control-static")
        self.assertTrue(dlsform.fields['recipient'].widget.attrs.get("class")=="form-control-static")
        self.assertIsInstance(dlsform.fields['delivery_line_id'].widget, widgets.HiddenInput)
        self.assertIsInstance(dlsform.fields['selected'], BooleanField)
        #todo:work here!

##MODELTESTS
class ModelTest(TestCase):

    def test_can_save_and_retrieve_Invoice_and_InvoiceLine(self):
        i1 = createTestInvoice()
        i1l1 = createTestInvoiceLine(i1)
        i1l2 = createTestInvoiceLine(i1)
        i2 = createTestInvoice()
        i2l1 = createTestInvoiceLine(i2)

        saved_invoices = Invoice.objects.all()
        self.assertEqual(saved_invoices.count(), 2)
        self.assertEqual(InvoiceLine.objects.all().count(),3)

        first_saved_invoice = saved_invoices[0]
        second_saved_invoice = saved_invoices[1]
        self.assertEqual(first_saved_invoice.invoice_no, i1.invoice_no)
        self.assertEqual(second_saved_invoice.invoice_no, i2.invoice_no)
        self.assertEqual(second_saved_invoice.invoiceline_set.count(), 1)
        self.assertEqual(second_saved_invoice.invoiceline_set.last().product, i2l1.product)


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

    def test_can_save_and_retrieve_Delivery_and_DeliveryLine(self):
        first_delivery = Delivery()
        first_delivery.dlry_no = "FirstDeliveryNo"
        first_delivery.recipient = "FirstCustomer"
        first_delivery.dispatch_date='2015-05-05'
        first_delivery.save()

        second_delivery = Delivery()
        second_delivery.dlry_no = "2ndDeliveryNo"
        second_delivery.recipient = "2ndCustomer"
        second_delivery.dispatch_date='2015-05-10'
        second_delivery.save()

        o = createTestOrder()
        ol = createTestOrderLine(o)

        dL = DeliveryLine()
        dL.delivery_id=second_delivery.id
        dL.order_line_id = ol.id
        dL.product = 'aGuide'
        dL.qty = 25.5
        dL.save()

        dL2 = DeliveryLine()
        dL2.delivery_id=second_delivery.id
        dL2.product = 'aGuide'
        dL2.qty = 25.5
        dL2.save()

        saved_deliveries = Delivery.objects.all()
        self.assertEqual(saved_deliveries.count(), 2)
        self.assertEqual(DeliveryLine.objects.all().count(),2)

        first_saved_delivery = saved_deliveries[0]
        second_saved_delivery = saved_deliveries[1]
        self.assertEqual(first_saved_delivery.dlry_no, 'FirstDeliveryNo')
        self.assertEqual(second_saved_delivery.dlry_no, '2ndDeliveryNo')
        self.assertEqual(second_saved_delivery.deliveryline_set.count(), 2)
        self.assertEqual(second_saved_delivery.deliveryline_set.last().product, 'aGuide')
        self.assertEqual(second_saved_delivery.deliveryline_set.first().order_line_id, ol.id)
