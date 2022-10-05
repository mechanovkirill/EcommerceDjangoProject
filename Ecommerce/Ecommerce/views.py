from django.views.generic import TemplateView
from store.models import Product
from django.shortcuts import render


def home_view(request):
    products = Product.objects.all().filter(is_available=True)

    return render(request, 'home.html', context={'products': products})
    # путь прописан в settings.py, templates DIR ('templates')
