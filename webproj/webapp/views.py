from django.shortcuts import render
import logging

# Настраиваем логирование
logger = logging.getLogger(__name__)

def index(request):
    html = """
    <h1>Мой первый Django сайт!</h1>
    <p>Меня зовут Глеб</p>
    <p>На этом сайте я буду делиться своими проектами и опытом в программировании.</p>
    """
    logging.info(f"Пользователь посетил страницу 'главная'")
    return render(request, 'index.html', {'html': html})


def about(request):
    html = """
    <h1>Обо мне</h1>
    <p>Что то обо мне:</p>
    <p>Я увлекаюсь созданием сайтов и приложений, особенно с использованием Django.</p>
    """
    logging.info(f"Пользователь посетил страницу 'о себе'")
    return render(request, 'about.html', {'html': html})