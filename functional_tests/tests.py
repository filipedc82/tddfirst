from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
from django.test.utils import override_settings
from orderlist.models import *
from orderlist.tests import createTestOrderLine, \
                            createTestOrder, \
                            createTestDelivery, \
                            createTestDeliveryLine, \
                            createTestInvoice, \
                            createTestInvoiceLine, \
                            createTestProduct


@override_settings(DEBUG=True)
class ProductListTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        #setattr(settings, 'DEBUG', true)

    def tearDown(self):
        self.browser.quit()
      #  pass


    def test_can_see_product_info(self):
        createTestProduct()
        # Klaus opens the browser and goes to the products page
        self.browser.get(self.live_server_url+ "/products/")
        self.browser.set_window_size(1024, 768)

        # He notices the page title Product List and the styled page, and sees one product
        self.assertIn('Product List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Product', header_text)
        self.assertGreater(self.browser.find_element_by_tag_name('h1').location['x'], 10)
        self.assertIn("MyProduct", self.browser.find_element_by_tag_name('body').text)

        self.fail("Finish the test")

@override_settings(DEBUG=True)
class OrderListTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        #setattr(settings, 'DEBUG', true)

    def tearDown(self):
        self.browser.quit()
      #  pass


    def test_can_add_new_invoice(self):
        #prepare Orders and Invoices
        o1 = createTestOrder()
        ol1 = createTestOrderLine(o1)
        ol2 = createTestOrderLine(o1)
        o2 = createTestOrder()
        ol3 = createTestOrderLine(o2)
        ol4 = createTestOrderLine(o2)
        i1 = createTestInvoice()
        il1 = createTestInvoiceLine(i1)
        il2 = createTestInvoiceLine(i1)
        d1 = createTestDelivery()
        d1l1 = createTestDeliveryLine(d1)
        d1l2 = createTestDeliveryLine(d1)
        d2 = createTestDelivery()
        d2l1 = createTestDeliveryLine(d2)
        d2l2 = createTestDeliveryLine(d2)


        # Klaus opens the browser and goes to the invoice page
        self.browser.get(self.live_server_url+ "/invoices/")
        self.browser.set_window_size(1024, 768)

        # He notices the page title Invoice List and the styled page, and sees one invoice
        self.assertIn('Invoice List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Invoice', header_text)
        self.assertGreater(self.browser.find_element_by_tag_name('h1').location['x'], 10)
        self.assertIn(i1.invoice_no, self.browser.find_element_by_tag_name('body').text)

        # He clicks on the first invoice and is shown the invoice details
        self.browser.find_element_by_id("id_invoice_table").find_element_by_tag_name('a').click()

        # He clicks the return link and is returned to the invoice list
        self.browser.find_element_by_id("invoice_list_link").click()
        self.assertIn('Invoice List', self.browser.title)

        # He clicks the link to create a new Invoice
        create_link = self.browser.find_element_by_id('create_invoice_link')
        self.assertEqual(create_link.text,'Create new invoice')
        self.browser.get(self.live_server_url+ "/invoices/add/")

        # A window titled "select delivery lines for invoice" is displayed displaying the six delivery lines
        self.assertIn('Select Delivery Lines for new invoice', self.browser.find_element_by_tag_name('h1').text)
        body = self.browser.find_element_by_tag_name('body')
        self.assertTrue(body.text.count("Selected:")==6)

        # He selects the lines 3, 5, and 6, hits the confirm button #todo check that he cant edit
        self.browser.find_element_by_id('id_form-2-selected').click()
        self.browser.find_element_by_id('id_form-4-selected').click()
        self.browser.find_element_by_id('id_form-5-selected').click()
        self.browser.find_element_by_id('id_submit_select_delivery_lines_button').click()

        # He is redirected to a new page for adding invoice showing three prefilled lines and two extra lines
        self.assertIn('Add Invoice', self.browser.title)
        mgmtforminitial = self.browser.find_element_by_id('id_form-INITIAL_FORMS')
        self.assertEqual(mgmtforminitial.get_attribute("value"), '3')
        mgmtformtotal = self.browser.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(mgmtformtotal.get_attribute("value"), '5')

        # He enters header info, changes the qty on line 1, the unit price on line 2 and enters an additional position, then hits confirm button
        self.browser.find_element_by_id('id_invoice_no').send_keys("Invoice0815")
        self.browser.find_element_by_id('id_debitor').send_keys("myDebitor")
        self.browser.find_element_by_id('id_invoice_date').send_keys("2015-05-05")
        self.browser.find_element_by_id('id_form-0-qty').send_keys("120")
        self.browser.find_element_by_id('id_form-1-unit_price').send_keys("20.5")
        self.browser.find_element_by_id('id_form-3-product').send_keys("YAGuide")
        self.browser.find_element_by_id('id_form-3-qty').send_keys("10")
        self.browser.find_element_by_id('id_form-3-unit_price').send_keys("10")

        self.browser.find_element_by_id('id_submit_invoice_button').click()

        # He is redirected to a detail page showing the invoice details
        self.assertIn('Invoice Invoice0815', self.browser.title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("Invoice0815", body.text)
        self.assertIn("myDebitor", body.text)
        self.assertIn("YAGuide", body.text)
        self.assertTrue(body.text.count("uide")==4)


    def test_can_add_new_delivery(self):
        #prepare Orders
        o1 = createTestOrder()
        ol1 = createTestOrderLine(o1)
        ol2 = createTestOrderLine(o1)
        o2 = createTestOrder()
        ol3 = createTestOrderLine(o2)
        ol4 = createTestOrderLine(o2)

        # Klaus opens the browser and goes to the delivery page
        self.browser.get(self.live_server_url+ "/deliveries/")
        self.browser.set_window_size(1024, 768)


        # He notices the page title Delivery List and the styled page
        self.assertIn('Delivery List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Delivery', header_text)
        self.assertGreater(self.browser.find_element_by_tag_name('h1').location['x'], 10)

        # He clicks the link to create a new Delivery
        create_link = self.browser.find_element_by_id('create_delivery_link')
        self.assertEqual(create_link.text,'Create new delivery')
        self.browser.get(self.live_server_url+ "/deliveries/add/")

        # A window titled "select order lines for delivery" is displayed displaying the four open order lines (orderno, product, open_qty, dlry_date)

        self.assertIn('Select Order Lines for new delivery', self.browser.find_element_by_tag_name('h1').text)

        body = self.browser.find_element_by_tag_name('body')
        self.assertTrue(body.text.count("Selected:")==4)

        # He can't edit some other fields but selects order lines 1-3 and clicks the "Confirm Selection" #todo: check that he can't edit
        self.assertTrue(self.browser.find_element_by_id('id_form-0-product').get_attribute("class")=="form-control-static")
        self.browser.find_element_by_id('id_form-0-selected').click()
        self.browser.find_element_by_id('id_form-1-selected').click()
        self.browser.find_element_by_id('id_form-3-selected').click()
        self.browser.find_element_by_id('id_submit_select_order_lines_button').click()


        # A new page opens allowing to add a new delivery and 3 lines prefilled and two extra lines
        self.assertIn('Add Delivery', self.browser.title)
        mgmtforminitial = self.browser.find_element_by_id('id_form-INITIAL_FORMS')
        self.assertEqual(mgmtforminitial.get_attribute("value"), '3')
        mgmtformtotal = self.browser.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(mgmtformtotal.get_attribute("value"), '5')


        # A text field is showing prompting to enter the Delivery no, dispatch date, sender and recipient name
        delivery_no_field = self.browser.find_element_by_id('id_delivery_no')
        self.assertEqual(delivery_no_field.get_attribute('placeholder'), 'Delivery Number')
        recipient_field = self.browser.find_element_by_id('id_recipient')
        self.assertEqual(recipient_field.get_attribute('placeholder'), 'Recipient')
        sender_field = self.browser.find_element_by_id('id_sender')
        self.assertEqual(sender_field.get_attribute('placeholder'), 'Sender')
        date_field = self.browser.find_element_by_id('id_dispatch_date')
        self.assertEqual(date_field.get_attribute('placeholder'), 'Dispatch Date')


        # He enters header data, changes a qty, adds a line  and clicks the Button "Save delivery"
        delivery_no_field.send_keys("Dlry08/15")
        recipient_field.send_keys("MWH")
        sender_field.send_keys("DCA")
        date_field.send_keys("2015-07-07")
        self.browser.find_element_by_id("id_form-1-qty").send_keys("456")
        self.browser.find_element_by_id("id_form-3-product").send_keys("Anotherguide")
        self.browser.find_element_by_id("id_form-3-qty").send_keys("123")
        self.browser.find_element_by_id("id_submit_delivery_button").click()

        # He is redirected to a detail page showing the delivery
        self.assertIn('Delivery Dlry08/15', self.browser.title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn("Dlry08/15", body.text)
        self.assertIn("MWH", body.text)
        self.assertIn("Anotherguide", body.text)
        self.assertIn("123", body.text)
        self.assertIn(o1.order_no, body.text)


        # He clicks the "Return to Delivery List" Button and sees the Delivery List with the Delivery entry.
        self.browser.find_element_by_id("delivery_list_link").click()
        self.assertIn('Delivery List', self.browser.title)


    def test_can_add_a_new_order(self):
        # Klaus opens the browser and goes to the orders page
        self.browser.get(self.live_server_url+ "/orders")
        self.browser.set_window_size(1024, 768)


        # He notices the page title Order List and the styled page
        self.assertIn('Orders', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Orders', header_text)
        self.assertGreater(self.browser.find_element_by_tag_name('h1').location['x'], 10)


        # On the page there is a link for creating a new order
        create_link = self.browser.find_element_by_id('create_order_link')
        self.assertEqual(create_link.text,'Create new order')
        # He clicks the link to create a new order
        self.browser.get(create_link.get_attribute('href'))

        # A new page opens with the title mentioning "Add new order"
        self.assertIn('Add Order', self.browser.title)

        # A text field is showing prompting to enter the order no and customer name
        order_no_field = self.browser.find_element_by_id('id_order_no')
        self.assertEqual(order_no_field.get_attribute('placeholder'), 'Enter Order Number')
        customer_field = self.browser.find_element_by_id('id_customer')
        self.assertEqual(customer_field.get_attribute('placeholder'), 'Customer')

        # He types in BE/4711/215 for order no and MWH for customer
        order_no_field.send_keys('BE/4711/215')
        customer_field.send_keys('MWH')

        #He clicks the submit button and is redirected to a details page for the order
        self.browser.find_element_by_id('id_submit_new_order_button').click()
        self.assertIn('BE/4711/215', self.browser.title)


        #He sees Input Fields for Product, Qty, Price, and Delivery Date .
        product_field = self.browser.find_element_by_id('id_product')
        self.assertEqual(product_field.get_attribute('placeholder'),'Enter Product')
        qty_field = self.browser.find_element_by_id('id_qty')
        self.assertEqual(qty_field.get_attribute('placeholder'),'Enter Qty')
        price_field = self.browser.find_element_by_id('id_unit_price')
        self.assertEqual(price_field.get_attribute('placeholder'),'Enter Unit Price')
        dlrydate_field = self.browser.find_element_by_id('id_dlry_date')
        self.assertEqual(dlrydate_field.get_attribute('placeholder'),'Enter Delivery Date')

        # He enters the following data "75.21.211", 200, 50.60, 2015-05-05
        product_field.send_keys('75.21.211')
        qty_field.send_keys('200')
        price_field.send_keys('50.60')
        dlrydate_field.send_keys('2015-05-05')

        # He clicks the button "Save Order Line". The entered data appears in a table below the Order header.
        self.browser.find_element_by_id('id_submit_new_order_line_button').click()

        self.assertIn('BE/4711/215', self.browser.title)
        cells = self.browser.find_element_by_id('id_order_line_table').find_elements_by_tag_name('td')
        self.assertTrue(
            any(cell.text == '75.21.211' for cell in cells)
        )
        self.assertTrue(
            any(cell.text == '50.6' for cell in cells)
        )

        # He is returns to the order list page using the link.
        create_link = self.browser.find_element_by_id('order_list_link')
        self.assertEqual(create_link.text,'Back to Order List')
        self.browser.get(create_link.get_attribute('href'))

        #The new order shows in the list

        self.assertIn('Orders', self.browser.title)
        table = self.browser.find_element_by_id('id_order_table')
        cells = table.find_elements_by_tag_name('td')

        self.assertTrue(
            any(cell.text == 'MWH' for cell in cells)
        )
        self.assertTrue(
            any(cell.text == 'BE/4711/215' for cell in cells)
        )

        # He reloads the page and still finds the same order.
        self.browser.get(self.live_server_url+ "/orders")
#        time.sleep(10)
        table = self.browser.find_element_by_id('id_order_table')
        cells = table.find_elements_by_tag_name('td')
        self.assertTrue(
            any(cell.text == 'MWH' for cell in cells)
        )
        self.assertTrue(
            any(cell.text == 'BE/4711/215' for cell in cells)
        )

