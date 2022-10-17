from django.views.generic import TemplateView
from store.models import Product
from django.shortcuts import render
from django.core.paginator import Paginator


def home_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('product_name')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
    }


    return render(request, 'home.html', context=context)
    # путь прописан в settings.py, templates DIR ('templates')
