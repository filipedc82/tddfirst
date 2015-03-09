from django.forms import Form, ModelForm, CharField, TextInput
from orderlist.models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_no':TextInput(attrs={'placeholder':"Enter Order Number"}),
            'customer':TextInput(attrs={'placeholder':"Customer"}),
        }

