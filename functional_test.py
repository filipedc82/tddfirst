
from selenium import webdriver
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_new_order(self):
        # Klaus opens the browser and goes to the home page
        self.browser.get('http://localhost:8000/orders')

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

        # He types in BE/4711/215 for order no and MWH for customer and clicks the submit button
        order_no_field.send_keys('BE/4711/215')
        customer_field.send_keys('MWH')
       #Todo: Add orderlines to the order
        self.browser.find_element_by_id('id_submit_new_order_button').click()

        # He is returned to the order list page with the new order showing in the list.
        self.browser.get('http://localhost:8000/orders')
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
        self.browser.get('http://localhost:8000/orders/')
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


if __name__ == '__main__':
    unittest.main(warnings='ignore')