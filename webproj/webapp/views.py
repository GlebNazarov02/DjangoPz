from django.shortcuts import render
import logging
from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from webapp.models import Client, Order, OrderItem
# Настраиваем логирование
logger = logging.getLogger(__name__)

def index(request):
    html = ("<a href='/'>Home</a>&nbsp;&nbsp;"
            "<a href='/about/'>About</a>&nbsp;&nbsp;"
            "<a href='/clients'>Clients</a>"
            "<h1>Мой первый Django сайт!</h1>"
            "<p>Меня зовут Глеб</p>"
            "<p>На этом сайте я буду делиться своими проектами и опытом в программировании.</p>"
            )
    return HttpResponse(html)


def about(request):
    html = ("<a href='/'>Home</a>&nbsp;&nbsp;"
            "<a href='/about/'>About</a>&nbsp;&nbsp;"
            "<a href='/clients'>Clients</a>"
            "<h1>Обо мне<</h2>"
            "<h3>Что то обо мне:</h3>"
            "<p>Я увлекаюсь созданием сайтов и приложений, особенно с использованием Django.</p>"
            )
    return HttpResponse(html)


def clients_list(request):
    clients = Client.objects.all()

    html = ("<a href='/'>Home</a>&nbsp;&nbsp;"
            "<a href='/about/'>About</a>&nbsp;&nbsp;"
            "<a href='/clients'>Clients</a>"
            "<h1>Clients list</h2>"
            "<table>"
            "<tr><td>Name</td><td>E-mail</td><td>Phone</td><td>Address</td></tr>"
            )
    for client in clients:
        html += ("<tr>"
                 f"<td>{client.client_name}</td>"
                 f"<td>{client.email}</td>"
                 f"<td>{client.phone}</td>"
                 f"<td>{client.address}</td>"
                 "</tr>")
    html += "</table>"
    return HttpResponse(html)

def clients_orders(request, client_id):
    client = Client.objects.get(pk=client_id)
    orders = Order.objects.filter(client=Client)

    orders_products = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        product_counted = []
        for item in order_items:
            product = item.product
            quantity = item.product_count
            product_counted.append((product, quantity))
        orders_products.append((order,product_counted))

    context = {'orders_products': orders_products, 'Client': client}
    return render(request, "webapp/client.html", context)


def show_orders_period(request, client_id):
    now = timezone.now()  
    periods = {
        'week': now - timedelta(days=7),  
        'month': now - timedelta(days=30),
        'year': now - timedelta(days=365),
    }

    orders_data = {}
    client = Client.objects.get(pk=client_id)

    for period, start_date in periods.items():
        orders_data[period] = OrderItem.objects.filter(
            order__client=client,     
            order__date_ordered__gte=start_date   
        ).select_related('order', 'product').order_by('-order__date_ordered')

    context = {
        'orders_data': orders_data,
        'client': client
    }
    return render(request, "webapp/recent_orders.html", context)