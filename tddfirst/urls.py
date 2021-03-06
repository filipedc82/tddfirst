from django.conf.urls import patterns, include, url
#from django.contrib import admin
from orderlist import views
# from products import views
import products


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'orderlist.views.home_page', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^orders/$', views.OrderListView.as_view(), name='order_list'),
 #   url(r'^orders/$', 'orderlist.views.order_list', name='order_list'),
    url(r'^orders/(?P<pk>\d+)/$', views.OrderDetailView.as_view(), name='order_detail'),
    url(r'^orders/add/$', 'orderlist.views.add_order', name='add_order'),

    url(r'^deliveries/$', views.DeliveryListView.as_view(), name='delivery_list'),
    url(r'^deliveries/(?P<pk>\d+)/$', views.DeliveryDetailView.as_view(), name='delivery_detail'),
    url(r'^deliveries/add/(?P<olsid>.+)$', 'orderlist.views.add_delivery', name='add_delivery'),
    url(r'^deliveries/add/$', 'orderlist.views.select_ol', name='select_ol'),

    url(r'^invoices/$', views.InvoiceListView.as_view(), name='invoice_list'),
    url(r'^invoices/(?P<pk>\d+)/$', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    url(r'^invoices/add/(?P<dlsid>.+)$', 'orderlist.views.add_invoice', name='add_invoice'),
    url(r'^invoices/add/$', 'orderlist.views.select_dl', name='select_dl'),

#    url(r'^products/$', views.ProductListView.as_view(), name='product_list'),
    url(r'^products/$', include('products.urls'), name='product_list'),
)


### firstDjango code without generic views
# urlpatterns = patterns('',
#     # ex: /myDjangoApp/
#     url(r'^$', views.index, name='index'),
#
#     # ex: /myDjangoApp/5/
#     url(r'^specifics/(?P<question_id>\d+)/$', views.detail, name='detail'),
#
#     # ex: /myDjangoApp/5/results/
#     url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
#
#     # ex: /myDjangoApp/5/vote/
#     url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
#
# )