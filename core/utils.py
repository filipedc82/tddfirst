__author__ = 'Filipe'
from orderlist.models import Order,OrderLine,Delivery, DeliveryLine, Invoice, InvoiceLine, OwnProduct
from products.models import Product

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
    dlry.delivery_no = str(Delivery.objects.count()+815)
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

def createTestProduct(product_group="VG", opno=None):
    if opno is None:
        opno = "MyProduct%s" % Product.objects.count()
    p = Product()
    p.product_group = product_group
    p.own_product_no = opno
    p.save()
    return p