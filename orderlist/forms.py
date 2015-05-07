from django import forms
from orderlist.models import Order,OrderLine,Delivery, DeliveryLine, Invoice, InvoiceLine

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_no':forms.TextInput(attrs={'placeholder':"Enter Order Number", 'class':"form-control"}),
            'customer':forms.TextInput(attrs={'placeholder':"Customer", 'class':"form-control"}),
        }

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = '__all__'
        widgets = {
            'order': forms.HiddenInput(),
            'qty': forms.NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'unit_price': forms.NumberInput(attrs={'placeholder':"Enter Unit Price", 'class':"form-control"}),
            'product': forms.TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'dlry_date': forms.DateInput(attrs={'placeholder':"Enter Delivery Date",'class':"form-control",}),
            #      'customer':TextInput(attrs={'placeholder':"Customer", 'class':"form-control"}),
        }

class OrderLineSelectForm(forms.Form):
    product = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_no = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_qty = forms.FloatField(widget=forms.NumberInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_line_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    customer = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    selected = forms.BooleanField(required=True)

class DeliveryLineSelectForm(forms.ModelForm):
    delivery_date = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    recipient = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    delivery_no = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    delivery_line_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    selected = forms.BooleanField(required=True)

    class Meta:
        model = DeliveryLine
        fields = {'product', 'qty'}
        widgets = {
            'delivery_no': forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
            'product': forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
            'qty': forms.NumberInput(attrs={'readonly':'readonly', 'class':"form-control-static"}),
        }

class InvoiceLineForm(forms.ModelForm):
    delivery_no = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    order_no = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static"}))
    class Meta:
        model = InvoiceLine
        fields = ("product", "qty", "order_line","unit_price", "delivery_line")
        widgets = {
            'product': forms.TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'qty': forms.NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'unit_price': forms.NumberInput(attrs={'placeholder':"Enter Unit Price", 'class':"form-control"}),
            'delivery_line': forms.HiddenInput(),
            'order_line': forms.HiddenInput(),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'invoice_no': forms.TextInput(attrs={'placeholder':"Invoice Number", 'class':"form-control"}),
            'debitor': forms.TextInput(attrs={'placeholder':"Debitor", 'class':"form-control"}),
            'invoice_date': forms.DateInput(attrs={'placeholder':"invoice Date",'class':"form-control",}),
        }

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'
        widgets = {
            'delivery_no': forms.TextInput(attrs={'placeholder':"Delivery Number", 'class':"form-control"}),
            'recipient': forms.TextInput(attrs={'placeholder':"Recipient", 'class':"form-control"}),
            'sender': forms.TextInput(attrs={'placeholder':"Sender", 'class':"form-control"}),
            'dispatch_date': forms.DateInput(attrs={'placeholder':"Dispatch Date",'class':"form-control",}),
        }

class DeliveryLineForm(forms.ModelForm):
    order_no = forms.CharField(max_length=50,required=False, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':"form-control-static", "readonly":"readonly"}))
    class Meta:
        model = DeliveryLine
        fields = ("product", "qty", "order_line")
        widgets = {
            'product': forms.TextInput(attrs={'placeholder':"Enter Product", 'class':"form-control"}),
            'qty': forms.NumberInput(attrs={'placeholder':"Enter Qty", 'class':"form-control"}),
            'order_line': forms.HiddenInput(),
        }
