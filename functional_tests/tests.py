from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
from django.test.utils import override_settings
from orderlist.models import *

@override_settings(DEBUG=True)\

def createTestOrder():
    order = Order()
    order.order_no = str(Order.objects.count()+4711)
    order.customer = "Lego"
    order.save()
    ol1 = OrderLine()
    ol1.order = order
    ol1.dlry_date = '2015-05-05'
    ol1.product = 'anotherGuide'
    ol1.unit_price = 10.0
    ol1.qty = 200
    ol1.save()
    ol2 = OrderLine()
    ol2.order = order
    ol2.dlry_date = '2015-05-10'
    ol2.product = 'anotherGuide2'
    ol2.unit_price = 12.0
    ol2.qty = 300
    ol2.save()
    return order



class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
#        setattr(settings, 'DEBUG', true)

    def tearDown(self):
        self.browser.quit()





    def test_addOrder(self):
        o1 = createTestOrder()
        print(o1.order_no)
        o2 = createTestOrder()
        print(o2.order_no)
        self.fail()

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

        self.fail('Finish the test!')

