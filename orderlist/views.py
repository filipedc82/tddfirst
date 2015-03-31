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
    dlformset = formset_factory(DeliveryLineForm, extra=2)
    if request.method == 'POST':
        print("debug1")
        dform = DeliveryForm(request.POST)
        dlforms = dlformset(request.POST, request.FILES)
        if (dform.is_valid()):
            print("Hello dform")
            if (dlforms.is_valid()):
                print("Hello dlforms")
                newD= dform.save(commit=True)
                print(newD.id)
                print(dlforms.cleaned_data)
                for dataset in dlforms.cleaned_data:
                    if dataset:
                        newDL = DeliveryLine()
                        newDL.delivery = newD
                        newDL.product= dataset.get('product')
                        newDL.qty = dataset.get('qty')
                        if dataset.get("order_line"):
                            newDL.order_line_id = int(dataset.get("order_line").id)
                        newDL.save()
                        print("Yeah "+str(newDL))
                return redirect(newD.get_absolute_url())




                # for dlform in dlforms:
                #     print(dlform)
                #     if dlform.is_valid():
                #         print("Going in")
                #         print(dlform)
                #         newDL=dlform.save(commit=False)
                #         newDL.delivery_id = newD.id
                #         newDL.order_line_id = 1
                #         newDL.save()
                # newD.save()

            else:
                print(dlforms.errors)
        else:
            print(dform.errors)
            #     new_order = form.save(commit=True)
            #     return redirect('/orders/'+str(new_order.id)+'/')
            #
            # else:
            #     print(form.errors)

    else:
        dform = DeliveryForm()

        olineids = olsid.split(",")[:-1]
        #todo: make robust to cope with forgotten trailing comma

        olines = []
        for olineid in olineids:
            olines.append(OrderLine.objects.get(pk=olineid))
        data = []
        for oline in olines:
            data.append({'order_no': oline.order_id,
                         'qty': oline.qty,
                         'product':oline.product,
                         'order_line':oline.id
                        })
        dlforms = dlformset(initial=data)

    return render(request, 'add_delivery.html',{'dform': dform,
                                                'dlforms': dlforms})






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
        for ol in OrderLine.objects.all():
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



def home_page(request):
    return render(request, 'home.html')
