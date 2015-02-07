from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_new_order(self):
        # Klaus opens the browser and goes to the home page
        self.browser.get('http://localhost:8000')

        # He notices the page title mentioning Orders
        self.assertIn('Orders', self.browser.title)

        # On the page there is a button for creating a new order
        self.
        # He hits the button to create a new order

        # On the page he finds a list of orders in a table. A new order appears

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')