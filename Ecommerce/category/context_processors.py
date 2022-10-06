from .models import Category

def menu_links(request):
    category_links = Category.objects.all()
    return dict(category_links=category_links)
"""
Контекстный процессор(context processor) — это функция Python, 
которая принимает объект запроса в качестве аргумента 
и возвращает словарь, добавляемый в контекст запроса. Они удобны, 
когда необходимо сделать что-то доступным для всех шаблонов."""