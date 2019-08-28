"""DOMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from orders import views as my_order
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', my_order.order_index, name='home'),
    url(r'^orders$', my_order.order_index, name='home'),
    url(r'^order/(?P<order_id>\d+)/$', my_order.show_order, name='show-order'),
    url(r'^order/new/$', my_order.new_order, name='new-order'),
    url(r'^order/edit/(?P<order_id>\d+)/$', my_order.edit_order, name='edit-order'),
    url(r'^order/delete/(?P<order_id>\d+)/$', my_order.destroy_order, name='delete-order'),

    url(r'^order/by-day$', my_order.order_by_day, name='order-by-day'),
    url(r'^order/by-month$', my_order.order_by_month, name='order-by-month'),
    url(r'^order/by-year$', my_order.order_by_year, name='order-by-year'),

    url(r'^books$', my_order.book_index, name='book-index'),
    url(r'^book/new/$', my_order.new_book, name='new-book'),
    url(r'^book/edit/(?P<book_id>\d+)/$', my_order.edit_book, name='edit-book'),
    url(r'^book/delete/(?P<book_id>\d+)/$', my_order.destroy_book, name='delete-book'),
    url(r'^book/rank$', my_order.book_rank, name='book-rank'),

    url(r'^customers$', my_order.customer_index, name='customer-index'),
    url(r'^customer/new/$', my_order.new_customer, name='new-customer'),
    url(r'^customer/edit/(?P<customer_id>\d+)/$', my_order.edit_customer, name='edit-customer'),
    url(r'^customer/delete/(?P<customer_id>\d+)/$', my_order.destroy_customer, name='delete-customer'),

    url(r'^users/login/$', auth.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^users/logout/$', auth.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^users/change_password/$',
        login_required(auth.PasswordChangeView.as_view(template_name='change_password.html', success_url='/')),
        name='change_password'),
]
