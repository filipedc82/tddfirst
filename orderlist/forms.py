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

