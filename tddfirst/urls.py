from django.conf.urls import patterns, include, url
#from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'orderlist.views.home_page', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^orders/$', 'orderlist.views.order_list', name='order_list'),

    url(r'^orders/add/$', 'orderlist.views.add_order', name='add_order'),

)
