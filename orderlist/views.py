from django.shortcuts import redirect, render
from django.http import HttpResponse
from orderlist.models import *

# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def order_list(request):
    if request.method == 'POST':
        new_order = Order()
        new_order.order_no = request.POST['order_no']
        new_order.customer = request.POST['customer']
        new_order.save()

        return redirect('/orders/')


    elif request.method == 'GET':
        orders = Order.objects.all()
        context_dict = {'orders': orders}
        return render(request, 'order_list.html', context_dict)


def add_order(request):
    return render(request, 'add_order.html')

