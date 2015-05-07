from django.shortcuts import render
from django.views import generic

from .models import Product


# Create your views here.
def home_page(request):
    return render(request, 'home.html')

class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'