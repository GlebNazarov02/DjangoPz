from django.shortcuts import render
import logging
from django.core.files.storage import FileSystemStorage
from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from webapp.models import Client, Order, OrderItem
from . import models
from . import forms
from django.shortcuts import render, redirect
from webapp.forms import ImageForm
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
        quantityed = []
        for item in order_items:
            product = item.product
            quantity = item.quantity
            quantityed.append((product, quantity))
        orders_products.append((order,quantityed))

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

def change_product(request, product_id):
    product = models.Product.objects.filter(pk=product_id).first()
    form = forms.ProductForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        image = form.cleaned_data['image']
        if isinstance(image, bool):
            image = None
        if image is not None:
            fs = FileSystemStorage()
            fs.save(image.name, image)
        product.pname = form.cleaned_data['name']
        product.description = form.cleaned_data['description']
        product.cost = form.cleaned_data['price']
        product.quantity = form.cleaned_data['amount']
        product.image = image
        product.save()
        return redirect('products')
    else:
        form = forms.ProductForm(initial={'name': product.pname, 'description': product.description,
                                          'price': product.cost, 'amount': product.quantity, 'image': product.image})

    return render(request, 'webapp/change_product.html', {'form': form})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
    else:
        form = ImageForm()
    return render(request, 'webapp/upload_image.html', {'form': form})