from django.shortcuts import render
import logging
from django.http import HttpResponse
from webapp.models import Client
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