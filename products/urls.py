__author__ = 'Filipe'
from django.conf.urls import patterns, include, url
# from django import views

from .views import home_page, ProductListView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', ProductListView.as_view(), name='product_list'),
    )
