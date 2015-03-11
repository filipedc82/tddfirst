from django.db import models
from django.core.urlresolvers import reverse

class Order(models.Model):
    order_no = models.TextField(max_length=50)
    customer = models.TextField(max_length=50)

    def __str__(self):
        return self.order_no

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})


class OrderLine(models.Model):
    order = models.ForeignKey(Order)
    product = models.TextField(max_length=50)
    qty = models.FloatField()
    unit_price = models.FloatField()
    dlry_date = models.DateField()


class Delivery(models.Model):
    dlry_no = models.TextField(max_length=50)
    recipient = models.TextField(max_length=50)
    sender = models.TextField(max_length=50)
    dispatch_date = models.DateField()


class DeliveryLine(models.Model):
    delivery = models.ForeignKey(Delivery)
    order_line = models.ForeignKey(OrderLine)
    product = models.TextField(max_length=50)
    qty = models.FloatField()