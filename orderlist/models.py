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

    def __str__(self):
        return str(self.id)


class Delivery(models.Model):
    delivery_no = models.TextField(max_length=50)
    recipient = models.TextField(max_length=50)
    sender = models.TextField(max_length=50)
    dispatch_date = models.DateField()

    def __str__(self):
        return self.delivery_no

    def get_absolute_url(self):
        return reverse('delivery_detail', kwargs={'pk': self.pk})


class DeliveryLine(models.Model):
    delivery = models.ForeignKey(Delivery)
    order_line = models.ForeignKey(OrderLine, blank=True, null=True)
    product = models.TextField(max_length=50)
    qty = models.FloatField()

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    invoice_no = models.TextField(max_length=50)
    debitor = models.TextField(max_length=50)
    invoice_date = models.DateField()

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse('invoice_detail', kwargs={'pk': self.pk})

    def get_invoice_value(self):
        value = 0
        for il in self.invoiceline_set.all():
            value = value + float(il.get_line_value())
        return str(value);


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice)
    order_line = models.ForeignKey(OrderLine, blank=True, null=True)
    delivery_line = models.ForeignKey(DeliveryLine, blank=True, null=True)
    product = models.TextField(max_length=50)
    qty = models.FloatField()
    unit_price = models.FloatField()

    def __str__(self):
        return str(self.id)

# todo: Check @cached Property
    def get_line_value(self):
        return str(self.qty*self.unit_price)

class OwnProduct(models.Model):
    PRODUCT_GROUPS = (
        ('VG', 'Valve Guide'),
        ('VS', 'Valve Seat'),
        ('EV', 'Engine Valve'),
        ('EVO', 'Engine Valve Other'),
        ('NGP', '(Normalien)Guide Pin'),
        ('NLS', '(Normalien)Limit Switch'),
        ('NLS', '(Normalien)Other'),
        ('O', 'Other'),
    )
    product_group = models.CharField(max_length=50, choices=PRODUCT_GROUPS, default="O")
    own_product_no = models.CharField(max_length=50)

    def __str__(self):
        return str(self.own_product_no)
