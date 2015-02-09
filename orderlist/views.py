from django.shortcuts import redirect, render,  get_object_or_404
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

        return redirect('/orders/'+str(new_order.id)+'/')


    elif request.method == 'GET':
        orders = Order.objects.all()
        context_dict = {'orders': orders}
        return render(request, 'order_list.html', context_dict)

def order_detail(request, order_id):
    order = get_object_or_404(Order,pk=order_id)
    print(order)
    context_dict = {'order': order}
    return render(request, 'order_detail.html', context_dict)


def add_order(request):
    return render(request, 'add_order.html')

