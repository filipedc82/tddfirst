from django.forms import Form, ModelForm, CharField, TextInput
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
        # widgets = {
        #      'order_no':TextInput(attrs={'placeholder':"Enter Order Number", 'class':"form-control"}),
        #      'customer':TextInput(attrs={'placeholder':"Customer", 'class':"form-control"}),
        #  }