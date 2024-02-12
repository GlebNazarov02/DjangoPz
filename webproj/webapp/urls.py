from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('clients/', views.clients_list, name='clients'),
    path('clients/<int:client_id>', views.clients_orders, name='clients_orders'),
    path('clients/orders/<int:client_id>', views.show_orders_period, name='show_orders_period')

]