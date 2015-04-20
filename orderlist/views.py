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

class InvoiceListView(generic.ListView):
    model = Invoice
    template_name = 'invoice_list.html'

class ProductListView(generic.ListView):
    model = OwnProduct
    template_name = 'product_list.html'


class DeliveryDetailView(generic.DetailView):
    model = Delivery
    template_name='delivery_detail.html'

class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name='invoice_detail.html'


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
        dform = DeliveryForm(request.POST)
        dlforms = dlformset(request.POST, request.FILES)
        if (dform.is_valid()):
            if (dlforms.is_valid()):
                newD= dform.save(commit=True)
                for dataset in dlforms.cleaned_data:
                    if dataset:
                        newDL = DeliveryLine()
                        newDL.delivery = newD
                        newDL.product= dataset.get('product')
                        newDL.qty = dataset.get('qty')
                        if dataset.get("order_line"):
                            newDL.order_line_id = int(dataset.get("order_line").id)
                        newDL.save()
                return redirect(newD.get_absolute_url())

            else:
                print(dlforms.errors)
        else:
            print(dform.errors)

    else:
        dform = DeliveryForm()
        olineids = olsid.split(",")[:-1]
        #todo: make robust to cope with forgotten trailing comma

        olines = []
        for olineid in olineids:
            olines.append(OrderLine.objects.get(pk=olineid))
        data = []
        for oline in olines:
            data.append({'order_no': oline.order.order_no,
                         'qty': oline.qty,
                         'product':oline.product,
                         'order_line':oline.id
                        })
        dlforms = dlformset(initial=data)

    return render(request, 'add_delivery.html',{'dform': dform,
                                                'dlforms': dlforms})


def add_invoice(request, dlsid):
    ilformset = formset_factory(InvoiceLineForm, extra=2)
    if request.method == 'POST':
        iform = InvoiceForm(request.POST)
        ilforms = ilformset(request.POST, request.FILES)
        if (iform.is_valid()):
            print("ilforms: "+str(ilforms))

            if (ilforms.is_valid()):
                newI= iform.save(commit=True)
                for dataset in ilforms.cleaned_data:
                    if dataset:
                        newIL = InvoiceLine()
                        newIL.invoice = newI
                        newIL.product= dataset.get('product')
                        newIL.qty = dataset.get('qty')
                        newIL.unit_price = dataset.get('unit_price')

                        if dataset.get("order_line"):
                            newIL.order_line_id = int(dataset.get("order_line").id)
                        if dataset.get("delivery_line"):
                            newIL.delivery_line_id = int(dataset.get("delivery_line").id)
                        newIL.save()
                return redirect(newI.get_absolute_url())

            else:
                print("ilforms errors: "+ str(ilforms.errors))
        else:
            print("iforms errors: "+str(iform.errors))

    else:
        iform = InvoiceForm()

        dlineids = dlsid.split(",")[:-1]
        #todo: make robust to cope with forgotten trailing comma

        dlines = []
        for dlineid in dlineids:
            dlines.append(DeliveryLine.objects.get(pk=dlineid))
        data = []
        for dline in dlines:
            data.append({'order_no': dline.order_line.order.order_no,
                         'delivery_no': dline.delivery.delivery_no,
                         'product':dline.product,
                         'qty': dline.qty,
                         'unit_price': dline.order_line.unit_price,
                         'delivery_line':dline.id,
                         'order_line': dline.order_line_id,
                        })
        ilforms = ilformset(initial=data)

    return render(request, 'add_invoice.html',{'iform': iform,
                                                'ilforms': ilforms})



def select_dl(request):
    if request.method == "POST":
        dl_string = ""
        for key in request.POST.keys():
            if ("selected" in key) and str(request.POST.get(key))== 'on' :
                dlsformno = key[key.index("-")+1:key.index("selected")-1]
                dlfield = "form-"+str(dlsformno)+"-delivery_line_id"
                dl_string = dl_string + str(request.POST.get(dlfield)) + ","
        return redirect('/invoices/add/'+dl_string)

    else:
        data = []
        for dl in DeliveryLine.objects.all():
             data.append({'delivery_line_id': dl.id,
                          'qty': dl.qty,
                          'delivery_no':dl.delivery.delivery_no,
                          'product': dl.product,
                          'recipient': dl.delivery.recipient,
                          'delivery_date':dl.delivery.dispatch_date
                          })
             print(data)
        fs = formset_factory(DeliveryLineSelectForm, extra=0)
        dlsforms = fs(initial = data)
        print("FORMS:")
        print(dlsforms)

        return render(request, 'select_dl.html', {'delivery_line_select_forms': dlsforms })


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
