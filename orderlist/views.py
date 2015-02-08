from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def add_order(request):
    return render(request, 'add_order.html')

