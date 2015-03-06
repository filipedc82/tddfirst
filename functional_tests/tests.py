from django.test import LiveServerTestCase
from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
from django.test.utils import override_settings

@override_settings(DEBUG=True)
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
#        setattr(settings, 'DEBUG', true)

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_new_order(self):
        # Klaus opens the browser and goes to the home page
        self.browser.get(self.live_server_url+ "/orders")

        # TODO: He is redirected to the order list page

        # He notices the page title mentioning Orders
        self.assertIn('Orders', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Orders', header_text)

        # On the page there is a link for creating a new order
        create_link = self.browser.find_element_by_id('create_order_link')
        self.assertEqual(create_link.text,'Create new order')
        # He hits the button to create a new order
        self.browser.get(create_link.get_attribute('href'))

        # A new page opens with the title mentioning "Add new order"
        self.assertIn('Add order', self.browser.title)

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


        #He clicks the Button "Add Order Line" and Input Fields for Product, Qty, Price, and Date appear.
        add_line_button = self.browser.find_element_by_id('id_add_line_button')
        self.assertEqual(add_line_button.text, 'Add Order Line')
        add_line_button.click()
        product_field = self.browser.find_element_by_id('id_product_field')
        self.assertEqual(product_field.get_attribute('placeholder'),'Enter Product')
        qty_field = self.browser.find_element_by_id('id_qty_field')
        self.assertEqual(qty_field.get_attribute('placeholder'),'Enter Qty')
        price_field = self.browser.find_element_by_id('id_price_field')
        self.assertEqual(price_field.get_attribute('placeholder'),'Enter Unit Price')
        dlrydate_field = self.browser.find_element_by_id('id_dlrydate_field')
        self.assertEqual(dlrydate_field.get_attribute('placeholder'),'Enter Delivery Date')

        # He enters the following data "75.21.211", 200, 50.60, 2015-05-05
        product_field.send_keys('75.21.211')
        qty_field.send_keys('200')
        price_field.send_keys('50.60')
        dlrydate_field.send_keys('2015-05-05')

        # He clicks the button "Save Order Line". The entered data appears in a table below the Order header.






        # He is returned to the order list page with the new order showing in the list.
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

#
#if __name__ == '__main__':
#    unittest.main(warnings='ignore')