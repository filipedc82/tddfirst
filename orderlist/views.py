from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpRequest
from django.views import generic
from orderlist.models import *
from orderlist.forms import *
from django.forms.formsets import formset_factory

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

def add_delivery(request, olsid):
    print('DEBUG add_delivery view')
    print(olsid.split(","))
    return render(request, 'add_delivery.html')


def select_ol(request):
    if request.method == "POST":
        ol_string = ""
        for key in request.POST.keys():
            if ("selected" in key) and str(request.POST.get(key))== 'on' :
                olsformno = key[key.index("-")+1:key.index("selected")-1]
                olfield = "form-"+str(olsformno)+"-order_line_id"
                ol_string = ol_string + str(request.POST.get(olfield)) + ","
        return redirect('/deliveries/add/'+ol_string)


    else:
        data = []
        for x in range(1, OrderLine.objects.count()+1):
            ol = OrderLine.objects.get(pk=x)
            data.append({'order_line_id': ol.id,
                         'order_qty': ol.qty,
                         'order_no':ol.order.order_no,
                         'product': ol.product,
                         'customer': ol.order.customer,
                         })
        fs = formset_factory(OrderLineSelectForm, extra=0)
        olsforms = fs(initial = data)


        return render(request, 'select_ol.html', {'order_line_select_forms': olsforms })


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
