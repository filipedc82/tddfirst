from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from orderlist.models import *
from orderlist.forms import *

class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


# def order_detail(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     context_dict = {'order': order}
#     return render(request, 'order_detail.html', context_dict)




def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            new_order = form.save(commit=True)
            return redirect('/orders/'+str(new_order.id)+'/')

        else:
            print(form.errors)

    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form':form})





        # new_order = Order()
        # new_order.order_no = request.POST['order_no']
        # new_order.customer = request.POST['customer']
        # new_order.save()
        # return redirect('/orders/'+str(new_order.id)+'/')







def home_page(request):
    return render(request, 'home.html')
