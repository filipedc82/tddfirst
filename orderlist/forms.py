from django.forms import *
from orderlist.models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_no':TextInput(attrs={'placeholder':"Enter Order Number", 'class':"form-control"}),
            'customer':TextInput(attrs={'placeholder':"Customer", 'class':"form-control"}),
        }

class OrderLineForm(ModelForm):
    class Meta:
        model = OrderLine
        fields = '__all__'
        widgets = {
            'order': HiddenInput(),
            'qty': NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'unit_price': NumberInput(attrs={'placeholder':"Enter Unit Price", 'class':"form-control"}),
            'product': TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'dlry_date': DateInput(attrs={'placeholder':"Enter Delivery Date",'class':"form-control",}),
            #      'customer':TextInput(attrs={'placeholder':"Customer", 'class':"form-control"}),
        }

class OrderLineSelectForm(Form):
    product = CharField(max_length=50, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_no = CharField(max_length=50, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_qty = FloatField(widget=NumberInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_line_id = IntegerField(required=False, widget=HiddenInput())
    customer = CharField(max_length=50, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    selected = BooleanField(required=True)

class DeliveryLineSelectForm(ModelForm):
    delivery_date = DateTimeField(widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    recipient = CharField(max_length=50, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    delivery_no = CharField(max_length=50, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    delivery_line_id = IntegerField(required=False, widget=HiddenInput())
    selected = BooleanField(required=True)

    class Meta:
        model = DeliveryLine
        fields = {'product', 'qty'}
        widgets = {
            'delivery_no': TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
            'product': TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
            'qty': NumberInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
        }

class InvoiceLineForm(ModelForm):
    delivery_no = CharField(max_length=50,required=False, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_no = CharField(max_length=50,required=False, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    class Meta:
        model = InvoiceLine
        fields = ("product", "qty", "order_line","unit_price", "delivery_line")
        widgets = {
            'product': TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'qty': NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'unit_price': NumberInput(attrs={'placeholder':"Enter Unit Price", 'class':"form-control"}),
            'delivery_line': HiddenInput(),
            'order_line': HiddenInput(),
        }

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'invoice_no': TextInput(attrs={'placeholder':"Invoice Number", 'class':"form-control"}),
            'debitor': TextInput(attrs={'placeholder':"Debitor", 'class':"form-control"}),
            'invoice_date': DateInput(attrs={'placeholder':"invoice Date",'class':"form-control",}),
        }

class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'
        widgets = {
            'dlry_no': TextInput(attrs={'placeholder':"Delivery Number", 'class':"form-control"}),
            'recipient': TextInput(attrs={'placeholder':"Recipient", 'class':"form-control"}),
            'sender': TextInput(attrs={'placeholder':"Sender", 'class':"form-control"}),
            'dispatch_date': DateInput(attrs={'placeholder':"Dispatch Date",'class':"form-control",}),
        }

class DeliveryLineForm(ModelForm):
    order_no = CharField(max_length=50,required=False, widget=TextInput(attrs={'readonly':'readonly', 'class':"form-control-static", "readonly":"readonly"}))
    class Meta:
        model = DeliveryLine
        fields = ("product", "qty", "order_line")
        widgets = {
            'product': TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'qty': NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'order_line': HiddenInput(),
        }
