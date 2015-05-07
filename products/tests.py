from django.test import TestCase
from core.utils import *

# Create your tests here.
class ModelTest(TestCase):

    def test_can_save_and_retrieve_Product(self):
        p1 = createTestProduct()
        p2 = createTestProduct()

        saved_products = Product.objects.all()
        self.assertEqual(saved_products.count(), 2)

        first_saved_product = saved_products[0]
        second_saved_product = saved_products[1]
        self.assertEqual(first_saved_product.own_product_no, p1.own_product_no)
        self.assertEqual(second_saved_product.own_product_no, p2.own_product_no)
