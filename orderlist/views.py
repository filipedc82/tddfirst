from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpRequest
from django.views import generic
from orderlist.models import *
from orderlist.forms import *

class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'

class DeliveryListView(generic.ListView):
    model = Delivery
    template_name = 'delivery_list.html'


class DeliveryDetailView(generic.DetailView):
    model = Delivery
    template_name='delivery_detail.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        ol = OrderLine(order=context.get('order'))
        context['orderLineForm'] = OrderLineForm(instance=ol)
        return context



    def post(self, *args, **kwargs):
        olform = OrderLineForm(self.request.POST)
        if olform.is_valid():
            new_order_line = olform.save(commit=True)
            return redirect('/orders/'+str(self.request.POST.get('order'))+'/')
        else:
            print(olform.errors)
            new_request = HttpRequest()
            new_request.method = 'GET'
            new_request.path = '/orders/'+str(self.request.POST.get('order'))+'/'
            new_request.GET['orderLineForm']=olform
            #todo: Why does it not display errors on screen?
            return self.get(new_request, {'orderLineForm':olform})



# def order_detail(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     context_dict = {'order': order}
#     return render(request, 'order_detail.html's, context_dict)

def add_delivery(request):
    if request.method == "POST":
        print("POST DATA:")
        print(request.POST)

    olsforms = []
    for x in range(1, OrderLine.objects.count()+1):
         print("ol: "+str(x))
         ol = OrderLine.objects.get(pk=x)
         data = {'order_line_id': ol.id,
                 'order_qty': ol.qty,
                 'order_no':ol.order.order_no,
                 'product': ol.product,
                 'customer': ol.order.customer,
                 'selected': ol.id}
         print(data)
         newOlsform = OrderLineSelectForm(data) # todo: how to get different name space for each form? Try formsets
  #       newOlsform.selected.__setattr__({'id':"testing"})
         olsforms.append(newOlsform) #, prefix=str(x))
         print(olsforms[x-1])

    return render(request, 'add_delivery.html', {'order_line_select_forms': olsforms })


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
