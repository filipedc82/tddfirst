from django.shortcuts import render
from django.http import HttpResponse
from orderlist.models import *

# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def order_list(request):
    if request.method == 'POST':
        return render(request, 'order_list.html',
                      {'order_no': request.POST['order_no'], 'customer': request.POST['customer']})
    elif request.method == 'GET':
        orders = Order.objects.all()
        context_dict = {'orders': orders}
        return render(request, 'order_list.html', context_dict)


def add_order(request):
    return render(request, 'add_order.html')

